import streamlit as st
import streamlit.components.v1 as components
import os

# 1. Configuração da Página (Onde tudo começa)
st.set_page_config(
    page_title='LogiTrein 4.0', 
    layout='wide', 
    initial_sidebar_state='collapsed'
)

# 2. ONDE VOCÊ COLA O ESTILO (CSS para zerar as margens e esconder o lixo visual)
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
        }
        iframe {
            border: none;
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Lógica para carregar o seu HTML
current_dir = os.path.dirname(os.path.abspath(__file__))
# Tenta o nome longo ou qualquer .html que estiver lá
nome_do_arquivo = 'logitrein ULTIMA REVISÃO .html'
html_path = os.path.join(current_dir, nome_do_arquivo)

if not os.path.exists(html_path):
    for f in os.listdir(current_dir):
        if f.endswith('.html'):
            html_path = os.path.join(current_dir, f)
            break

if os.path.exists(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        html_data = f.read()
    
    # Exibe o sistema ocupando o máximo de espaço possível
    components.html(html_data, height=1200, scrolling=True)
else:
    st.error("Arquivo HTML não encontrado no GitHub.")
