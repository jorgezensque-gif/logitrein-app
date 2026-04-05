import streamlit as st
import streamlit.components.v1 as components
import os

# 1. CONFIGURAÇÃO DA PÁGINA (MODO AMPLO)
st.set_page_config(
    page_title='LogiTrein 4.0 - Sistema de Gestão', 
    layout='wide', 
    initial_sidebar_state='collapsed'
)

# 2. BLINDAGEM VISUAL (ESCONDE MENUS E ZERA ESPAÇOS BRANCOS)
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
        /* Ajuste fino para o expander de senhas não empurrar o sistema */
        .stExpander {
            margin: 10px 20px;
        }
    </style>
""", unsafe_allow_html=True)

# 3. LÓGICA DE LOCALIZAÇÃO DO ARQUIVO HTML
current_dir = os.path.dirname(os.path.abspath(__file__))
html_file = None

# Procura qualquer arquivo que termine com .html na pasta
for f in os.listdir(current_dir):
    if f.lower().endswith('.html'):
        html_file = os.path.join(current_dir, f)
        break

# 4. EXIBIÇÃO DO LOGITREIN
if html_file:
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_data = f.read()
        
        # Renderiza o sistema (ajuste o height se precisar de mais espaço)
        components.html(html_data, height=900, scrolling=True)
        
        # 5. GAVETA DE SEGURANÇA (RESTRITO AO JORGE)
        # Isso fica lá no final da página, bem discreto.
        with st.expander("🔑 ÁREA DO EDUCADOR (Consultar Acessos)"):
            st.warning("⚠️ Jovens: Acesso restrito ao coordenador do projeto.")
            st.markdown("""
            ### Tabela de Credenciais LogiTrein 4.0
            
            | Nível | Usuário | Senha | Perfil |
            | :--- | :--- | :--- | :--- |
            | **Conselho** | `jorge.zensque` | `master2026` | Admin Total |
            | **Gestão** | `gestor` | `gest123` | Supervisor |
            | **Líderes** | `lider.a` / `lider.b` / `lider.c` | `lid123` | Chefia de Turno |
            | **Operação** | `op01` até `op15` | `op123` | Jovens Aprendizes |
            """)
            
    except Exception as e:
        st.error(f"Erro ao ler o arquivo HTML: {e}")
else:
    st.error("❌ ERRO: Nenhum arquivo .html foi encontrado no seu GitHub!")
    st.info("Certifique se você subiu o arquivo 'logitrein ULTIMA REVISÃO .html' corretamente.")
