import streamlit as st
import streamlit.components.v1 as components
import os

# Configuração que remove a barra lateral e usa a largura total
st.set_page_config(
    page_title='LogiTrein 4.0', 
    layout='wide', 
    initial_sidebar_state='collapsed'
)

# CSS para esconder elementos do Streamlit e colar o HTML no topo
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 0rem;
            padding-right: 0rem;
        }
        iframe {
            border: none;
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

# Lógica para encontrar o seu arquivo HTML
current_dir = os.path.dirname(os.path.abspath(__file__))
nome_do_arquivo = 'logitrein ULTIMA REVISÃO .html'
html_path = os.path.join(current_dir, nome_do_arquivo)

# Se você renomeou para logitrein.html, o código abaixo garante que funcione
if not os.path.exists(html_path):
    for f in os.listdir(current_dir):
        if f.endswith('.html'):
            html_path = os.path.join(current_dir, f)
            break

if os.path.exists(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        html_data = f.read()
    
    # Height ajustado para 95% da altura da tela (vh)
    components.html(html_data, height=1200, scrolling=True)
else:
    st.error("Arquivo HTML não encontrado no GitHub.")
