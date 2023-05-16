from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import openpyxl
import re
import streamlit as st

url_imobiliaria = 'https://www.imobiliariaatual.com.br/'
url_base = 'https://www.imobiliariaatual.com.br/imoveis/locacao-pagina-'
def captura_dados():
  df = pd.DataFrame(columns=['Titulo','Endereço', 'Aluguel','Area','Descricao'])
  resp_inicial = requests.get(url_base+str(1))
  content_inicial = resp_inicial.content
  soup = BeautifulSoup(content_inicial, 'html.parser')
  n_imoveis = int(soup.find('p',class_='list__amount').text.strip().split(' ')[0])
  pags = n_imoveis//12
  progress_text = "Carregando dados, por favor aguarde."
  my_bar = st.progress(0, text=progress_text)
  progress = 1
  for i in range(int(pags)):
    cards_imoveis = obtem_cards_imoveis(pagina=i+1)
    for card_imovel in cards_imoveis:
      pag_imovel = acessa_pag_imovel(card_imovel)
      df_atual = manipula_e_extrai_pag_imovel(pag_imovel)
      df =  inclui_imovel_dataframe(df,df_atual)
      progress_percent = (progress / len(range(n_imoveis)))
      my_bar.progress(progress_percent, text=progress_text)     
      progress += 1
  my_bar.empty()    
  return df

def obtem_cards_imoveis(pagina):
  url_conteudo = url_base + str(pagina)
  soup = retorna_conteudo_pagina(url_conteudo)
  return soup.find_all('div', class_='list__hover')
def acessa_pag_imovel(card_imovel):
  link = extrai_link_card(card_imovel)
  return url_imobiliaria + link
def retorna_conteudo_pagina(link_pagina):
  resp = requests.get(link_pagina)
  content = resp.content
  return BeautifulSoup(content, 'html.parser')

def manipula_e_extrai_pag_imovel(pag_imovel):
  pagina = retorna_conteudo_pagina(pag_imovel)
  tipo_imovel = remove_linha_e_espaco_branco(pagina.find('h1', class_='card__type').text)
  endereco = remove_linha_e_espaco_branco(pagina.find('p', class_='card__address').text.split('(consulte a Imobiliária.).')[1].strip())
  infos = remove_linha_e_espaco_branco(obtem_infos(pagina))
  area = remove_linha_e_espaco_branco(obtem_metragem(infos))
  preco = remove_linha_e_espaco_branco(obtem_aluguel(pagina))
  return pd.DataFrame({'Titulo':[tipo_imovel],'Endereço': [endereco],'Aluguel': [preco],'Area': [area], 'Descricao':[infos]})

def extrai_link_card(card_imovel):
  return card_imovel.find('a',class_='list__link').get('href')  
def obtem_infos(pagina):
  infos = ''
  card_itens = pagina.find_all('div', class_='card__item')
  for i in range(len(card_itens)):
    infos += card_itens[i-1].find('p').text.strip()
    if i != len(card_itens) - 1:
      infos += ' ,'  
  return infos.strip()   
def obtem_aluguel(pagina):
  aluguel = pagina.find('div', class_='card__description-value').text
  if 'por:' in aluguel:
    aluguel = aluguel.split('por:')[1]
  return aluguel
def obtem_metragem(texto):  
  padrao = r"(\d+(\.\d+)?)\s*(m²|metros quadrados)"
  resultado = re.search(padrao, texto)
  if resultado:
    metragem_quadrada = resultado.group(0)
  else:
    metragem_quadrada = ""
  return metragem_quadrada
def remove_linha_e_espaco_branco(texto):
  texto = texto.replace('\n','')
  return " ".join(texto.split())

def inclui_imovel_dataframe(df,imovel):
  return pd.concat([df,imovel], ignore_index=True)



def exporta_df(df):
  return df.to_csv('dataframe_bruno.csv', index=False)
