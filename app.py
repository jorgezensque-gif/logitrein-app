import streamlit as st
import streamlit.components.v1 as components
import os

# 1. Configuração da Página
st.set_page_config(page_title='LogiTrein 4.0', layout='wide', initial_sidebar_state='collapsed')

# 2. Visual Blindado (Esconde menus e rodapés do Streamlit)
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container { padding: 0rem !important; }
        iframe { border: none; width: 100%; height: 100vh; }
    </style>
""", unsafe_allow_html=True)

# 3. Localização do HTML
current_dir = os.path.dirname(os.path.abspath(__file__))
nome_do_arquivo = 'logitrein ULTIMA REVISÃO .html'
html_path = os.path.join(current_dir, nome_do_arquivo)

# 4. Exibição do Sistema
if os.path.exists(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        html_data = f.read()
    # Exibe o sistema ocupando a tela inteira
    components.html(html_data, height=2000, scrolling=True)
else:
    st.error("Erro: Arquivo HTML não encontrado no repositório.")
