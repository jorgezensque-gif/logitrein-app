import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title='LogiTrein 4.0', layout='wide')

# O Streamlit vai ler o arquivo logitrein.html que você vai subir
with open('logitrein.html', 'r', encoding='utf-8') as f:
    html_data = f.read()

components.html(html_data, height=1200, scrolling=True)
