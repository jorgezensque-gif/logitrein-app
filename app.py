import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(page_title='LogiTrein 4.0', layout='wide')

# Pega o caminho absoluto da pasta onde o script está rodando
current_dir = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(current_dir, 'logitrein.html')

if os.path.exists(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        html_data = f.read()
    
    # Ajuste o height para 100vh (altura total da tela)
    components.html(html_data, height=1000, scrolling=True)
else:
    st.error(f"Arquivo 'logitrein.html' não encontrado. Verifique se o nome no GitHub está correto.")
