# -*- coding: utf-8 -*-
"""Mario_2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ND4YUXwTk-vKL1iRoFnW2tl3g8VN8fRR
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import openpyxl
import re

url_imobiliaria = 'https://www.imobiliariaatual.com.br/'

url_base = 'https://www.imobiliariaatual.com.br/imoveis/locacao-pagina-'
resp_inicial = requests.get(url_base+str(1))
content_inicial = resp_inicial.content
soup = BeautifulSoup(content_inicial, 'html.parser')
soup

n_imoveis = int(soup.find('p',class_='list__amount').text.strip().split(' ')[0])
n_imoveis

print(n_imoveis)

pags = n_imoveis//12
pags

df = pd.DataFrame(columns=['Titulo','Endereço', 'Aluguel','Area','Descricao'])

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
  return df.append({'Titulo':tipo_imovel,'Endereço': endereco,'Aluguel': preco,'Area': area, 'Descricao':infos},ignore_index=True)

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
  return pagina.find('div', class_='card__description-value').text
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

def inclui_imovel_dataframe(imovel):
  return pd.concat([df,imovel], ignore_index=True)

from pandas.core.arrays.interval import isin
itens_total = []
for i in range(int(pags)):
  cards_imoveis = obtem_cards_imoveis(pagina=i+1)
  itens_pag = []
  for card_imovel in cards_imoveis:
    pag_imovel = acessa_pag_imovel(card_imovel)
    df = manipula_e_extrai_pag_imovel(pag_imovel) 
df

pd.set_option('display.max_rows', None)

df

df.to_csv('./arquivo_imoveis_bruno.csv', index=False)

