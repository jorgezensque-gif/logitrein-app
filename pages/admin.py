import streamlit as st
import hashlib
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="Admin — Logitrein", page_icon="🔐", layout="wide")
st.markdown("""
<style>
html,body,[class*="css"]{font-family:'DM Sans',sans-serif!important;background:#09182e!important;color:#ddeaf8!important}
.main,section[data-testid="stMain"]{background:#09182e!important}
.block-container{padding:1.5rem 2rem!important;max-width:900px}
#MainMenu,footer,header,.stDeployButton{visibility:hidden!important;display:none!important}
</style>""", unsafe_allow_html=True)

ADMIN_HASH = hashlib.sha256("jorge2026master".encode()).hexdigest()
def checar_admin(s): return hashlib.sha256(s.encode()).hexdigest() == ADMIN_HASH
def file_exists(f): return (Path(__file__).parent.parent / f).exists()
def get_size(f):
    p = Path(__file__).parent.parent / f
    if not p.exists(): return "—"
    s = p.stat().st_size
    return f"{s/1024/1024:.1f} MB" if s>1024*1024 else f"{s/1024:.0f} KB"

if 'admin_ok' not in st.session_state: st.session_state.admin_ok = False

with st.sidebar:
    if st.button("← Voltar ao Portal"):
        st.session_state.admin_ok = False
        st.switch_page("app.py")

if not st.session_state.admin_ok:
    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
    _,col,_ = st.columns([1,1.4,1])
    with col:
        st.markdown("""<div style="background:#0f1929;border:1px solid rgba(245,200,66,.2);
        border-radius:14px;padding:32px 28px;text-align:center">
        <div style="font-size:2rem;margin-bottom:8px">🔐</div>
        <div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;color:#f5c842;margin-bottom:4px">Área Restrita</div>
        <div style="font-size:.75rem;color:#3a5070;margin-bottom:20px">Acesso exclusivo ao proprietário do sistema.</div>
        </div>""", unsafe_allow_html=True)
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        senha = st.text_input("", type="password", placeholder="Senha de administrador", label_visibility="collapsed")
        if st.button("🔓 Entrar", use_container_width=True):
            if checar_admin(senha):
                st.session_state.admin_ok = True; st.rerun()
            else:
                st.error("❌ Acesso negado.")
    st.stop()

# ── Painel admin autenticado ──
st.markdown("""<div style="padding:14px 18px;background:#0f1929;border:1px solid rgba(245,200,66,.2);
border-radius:12px;margin-bottom:20px">
<span style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;color:#f5c842">⚙️ Painel Administrativo</span>
<span style="font-size:.72rem;color:#5a7090;margin-left:12px">Jorge Zensque — Proprietário</span>
</div>""", unsafe_allow_html=True)

tab1,tab2,tab3 = st.tabs(["📁 Arquivos HTML","📊 Status","🔑 Segurança"])

with tab1:
    st.caption("Faça upload de versões novas dos sistemas.")
    c1,c2 = st.columns(2)
    with c1:
        for f in ['logitrein.html','logitrein_v12_integrado.html']:
            if file_exists(f): fname=f; break
        else: fname='logitrein.html'
        st.markdown(f"**🏭 Logitrein** — `{fname}`")
        st.caption(f"{'✅ '+get_size(fname) if file_exists(fname) else '❌ Não encontrado'}")
        up=st.file_uploader("Novo Logitrein HTML",type=['html'],key='up_lt')
        if up:
            (Path(__file__).parent.parent/'logitrein.html').write_bytes(up.read())
            st.success("✅ Atualizado!"); st.rerun()
    with c2:
        for f in ['logitrein_banco_v2.html','banco.html']:
            if file_exists(f): fname=f; break
        else: fname='logitrein_banco_v2.html'
        st.markdown(f"**🏦 Banco** — `{fname}`")
        st.caption(f"{'✅ '+get_size(fname) if file_exists(fname) else '❌ Não encontrado'}")
        up=st.file_uploader("Novo Banco HTML",type=['html'],key='up_bk')
        if up:
            (Path(__file__).parent.parent/'logitrein_banco_v2.html').write_bytes(up.read())
            st.success("✅ Atualizado!"); st.rerun()

with tab2:
    for fn,lb in [('logitrein.html','🏭 Logitrein'),('logitrein_banco_v2.html','🏦 Banco'),('app.py','⚙️ Portal'),('requirements.txt','📦 Requirements')]:
        ok=file_exists(fn); cor='#22c55e' if ok else '#e94b4b'
        st.markdown(f"<div style='display:flex;justify-content:space-between;padding:8px 12px;background:rgba(255,255,255,.03);border-radius:8px;margin-bottom:5px;font-size:.81rem'><span style='color:#c0d4e8'>{lb}</span><span style='color:{cor}'>{'✅ '+get_size(fn) if ok else '❌ Ausente'}</span></div>",unsafe_allow_html=True)
    st.caption(f"Verificado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

with tab3:
    st.markdown("##### Alterar senha")
    n1=st.text_input("Nova senha",type="password",placeholder="Mínimo 8 caracteres")
    n2=st.text_input("Confirmar",type="password",placeholder="Repita")
    if st.button("🔑 Gerar hash"):
        if len(n1)<8: st.error("Mínimo 8 caracteres.")
        elif n1!=n2: st.error("Senhas não conferem.")
        else:
            h=hashlib.sha256(n1.encode()).hexdigest()
            st.success("Cole no app.py E em pages/admin.py na linha ADMIN_HASH:")
            st.code(f'ADMIN_HASH = "{h}"', language="python")
    st.divider()
    if st.button("🚪 Sair"):
        st.session_state.admin_ok=False; st.switch_page("app.py")
