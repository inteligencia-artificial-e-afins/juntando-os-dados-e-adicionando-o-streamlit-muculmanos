import streamlit as st
from buche.exercicio import pegarDadosBuche
from lucas.lucas import pegarDadosLucas

BtnBuche = st.button("Carregar Dados - Buche")

if BtnBuche:
    data = pegarDadosBuche()
    st.dataframe(data)


BtnLucas = st.button("Carregar Dados - Lucas")

if BtnLucas:
    data = pegarDadosLucas()
    st.dataframe(data)