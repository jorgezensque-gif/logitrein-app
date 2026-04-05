import streamlit as st
import streamlit.components.v1 as components
import os

# Configuração da página
st.set_page_config(page_title='LogiTrein 4.0', layout='wide', initial_sidebar_state='collapsed')

# 1. Tentar encontrar o ficheiro de várias formas
current_dir = os.path.dirname(os.path.abspath(__file__))
ficheiros_na_pasta = os.listdir(current_dir)

# Nome que aparece no teu GitHub (com o espaço antes do ponto)
nome_especifico = 'logitrein ULTIMA REVISÃO .html'
html_data = None

# Lógica de busca blindada
if os.path.exists(os.path.join(current_dir, nome_especifico)):
    with open(os.path.join(current_dir, nome_especifico), 'r', encoding='utf-8') as f:
        html_data = f.read()
else:
    # Se não achou pelo nome, procura qualquer .html que esteja na pasta
    for f_nome in ficheiros_na_pasta:
        if f_nome.endswith('.html'):
            with open(os.path.join(current_dir, f_nome), 'r', encoding='utf-8') as f:
                html_data = f.read()
            break

# 2. Mostrar o conteúdo ou erro amigável
if html_data:
    # Remove margens do Streamlit para o HTML ocupar a tela toda
    st.markdown("""
        <style>
            .main > div { padding: 0; }
            iframe { border: none; }
        </style>
    """, unsafe_allow_html=True)
    
    components.html(html_data, height=1200, scrolling=True)
else:
    st.error("ERRO CRÍTICO: O sistema não encontrou nenhum ficheiro .html no GitHub.")
    st.write("Ficheiros detetados:", ficheiros_na_pasta)
    st.info("Dica: Garante que o ficheiro 'logitrein ULTIMA REVISÃO .html' foi subido corretamente.")
