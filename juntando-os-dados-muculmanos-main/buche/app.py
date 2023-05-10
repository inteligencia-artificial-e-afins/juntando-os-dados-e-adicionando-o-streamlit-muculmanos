import streamlit as st
import pandas as pd
import time

progress_text = "Carrgando dados, porfavor aguarde."
my_bar = st.progress(0, text=progress_text)

Btn = st.button("carregar dados")

if Btn:
    for percent_complete in range(100):
        time.sleep(0.1)
        data = pd.read_csv('scrapImobiliaria.csv')
        my_bar.progress(percent_complete + 1, text=progress_text)
    
    st.header("Dados da imobiliaria")

    st.dataframe(data)
