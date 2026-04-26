import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Banco Logitrein", page_icon="🏦", layout="wide")
st.markdown("""
<style>
html,body,[class*="css"]{background:#09182e!important}
.block-container{padding:0!important;margin:0!important;max-width:100%!important}
#MainMenu,footer,header,.stDeployButton{visibility:hidden!important;display:none!important}
</style>""", unsafe_allow_html=True)

with st.sidebar:
    if st.button("← Voltar ao Portal"):
        st.switch_page("app.py")

for f in ['logitrein_banco_v2.html','banco.html']:
    p = Path(__file__).parent.parent / f
    if p.exists():
        st.components.v1.html(p.read_text(encoding='utf-8'), height=950, scrolling=True)
        break
else:
    st.error("Arquivo banco não encontrado.")
