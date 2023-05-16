import streamlit as st
from buche.exercicio import pegarDadosBuche
from lucas.lucas import pegarDadosLucas
from bruno.bruno import captura_dados

BtnBuche = st.button("Carregar Dados - Buche")

if BtnBuche:
    data = pegarDadosBuche()
    st.dataframe(data)


BtnLucas = st.button("Carregar Dados - Lucas")

if BtnLucas:
    data = pegarDadosLucas()
    st.dataframe(data)

BtnBruno = st.button("Carregar Dados - Bruno")

if BtnBruno:
    data = captura_dados()
    st.dataframe(data)
