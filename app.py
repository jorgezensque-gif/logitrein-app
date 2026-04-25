"""
Logitrein + Banco — Portal de Acesso
Streamlit v3.0 — sistemas abrem em nova aba (resolve localStorage/login)
"""
import streamlit as st
import hashlib
import base64
from pathlib import Path
from datetime import datetime

st.set_page_config(
    page_title="Logitrein — Portal",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Senha admin hash SHA-256 (senha: jorge2026master)
ADMIN_HASH = hashlib.sha256("jorge2026master".encode()).hexdigest()
def checar_admin(s): return hashlib.sha256(s.encode()).hexdigest() == ADMIN_HASH

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif!important;background:#09182e!important;color:#ddeaf8!important}
.main,section[data-testid="stMain"]{background:#09182e!important}
.block-container{padding:2rem 2rem 1rem!important;max-width:1100px}
h1,h2,h3{font-family:'Syne',sans-serif!important}
.banner{background:linear-gradient(135deg,#112240,#0d2a55);border:1px solid rgba(0,201,167,.15);border-radius:16px;padding:32px 36px;margin-bottom:24px}
.brand{font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;color:#00c9a7}
.brand span{color:#f5c842}
.sub{font-size:.9rem;color:#7a9bbf;margin-top:4px}
.app-card{background:#132240;border:1px solid rgba(255,255,255,.07);border-radius:14px;padding:26px 22px;margin-bottom:14px;min-height:170px}
.card-title{font-family:'Syne',sans-serif;font-size:1.05rem;font-weight:700;color:#fff;margin-bottom:8px}
.card-desc{font-size:.82rem;color:#7a9bbf;line-height:1.6}
.card-hint{font-size:.72rem;color:#3a5070;margin-top:10px}
.badge{display:inline-block;padding:2px 9px;border-radius:99px;font-size:.58rem;font-weight:700;text-transform:uppercase;letter-spacing:.8px;margin-left:6px}
.b-teal{background:rgba(0,201,167,.14);color:#00c9a7}
.b-blue{background:rgba(26,86,219,.2);color:#93b4f7}
.b-gold{background:rgba(245,200,66,.15);color:#f5c842}
.metric-mini{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.07);border-radius:10px;padding:12px;text-align:center}
.m-label{font-size:.6rem;color:#7a9bbf;text-transform:uppercase;letter-spacing:.8px}
.m-val{font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700}
.info-box{background:rgba(0,201,167,.07);border:1px solid rgba(0,201,167,.18);border-radius:10px;padding:12px 16px;font-size:.8rem;color:#6ee7da;margin:10px 0;line-height:1.6}
.warn-box{background:rgba(245,200,66,.07);border:1px solid rgba(245,200,66,.2);border-radius:10px;padding:12px 16px;font-size:.8rem;color:#fde68a;margin:10px 0;line-height:1.6}
#MainMenu,footer,header,.stDeployButton{visibility:hidden!important;display:none!important}
</style>
""", unsafe_allow_html=True)

def file_exists(f): return (Path(__file__).parent / f).exists()
def get_size(f):
    p = Path(__file__).parent / f
    if not p.exists(): return "—"
    s = p.stat().st_size
    return f"{s/1024/1024:.1f} MB" if s > 1024*1024 else f"{s/1024:.0f} KB"
def html_to_b64(filename):
    p = Path(__file__).parent / filename
    if not p.exists(): return None
    return "data:text/html;base64," + base64.b64encode(p.read_bytes()).decode()
def lt_file():
    for f in ['logitrein.html','logitrein_v12_integrado.html']:
        if file_exists(f): return f
    return None
def banco_file():
    for f in ['logitrein_banco_v2.html','banco.html']:
        if file_exists(f): return f
    return None

for k,v in [('pagina','portal'),('admin_ok',False)]:
    if k not in st.session_state: st.session_state[k]=v

# SIDEBAR
with st.sidebar:
    st.markdown("""<div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:800;
    color:#00c9a7;padding:8px 0 14px;border-bottom:1px solid rgba(255,255,255,.07);margin-bottom:12px">
    🏦 Logitrein Portal</div>""", unsafe_allow_html=True)
    if st.button("🏠 Portal", use_container_width=True):
        st.session_state.pagina='portal'; st.rerun()
    if st.button("⚙️", key="btn_admin", help="Administração do sistema"):
        st.session_state.pagina='admin'; st.rerun()
    st.markdown(f"<div style='font-size:.6rem;color:#1e2d45;padding-top:20px'>v3.0 · {datetime.now().strftime('%d/%m/%Y')}</div>", unsafe_allow_html=True)

# PORTAL
def pagina_portal():
    lt_ok = lt_file() is not None
    bk_ok = banco_file() is not None

    st.markdown("""<div class="banner">
        <div class="brand">🏭 Logit<span>rein</span> · 🏦 Banco</div>
        <div class="sub">Portal integrado de gestão logística e financeira · Palmas/TO</div>
    </div>""", unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    with c1:
        cor='#22c55e' if lt_ok else '#e94b4b'
        st.markdown(f'<div class="metric-mini"><div class="m-label">Logitrein v12</div><div class="m-val" style="color:{cor}">{"✅ Online" if lt_ok else "❌ Offline"}</div></div>',unsafe_allow_html=True)
    with c2:
        cor='#22c55e' if bk_ok else '#e94b4b'
        st.markdown(f'<div class="metric-mini"><div class="m-label">Banco Logitrein</div><div class="m-val" style="color:{cor}">{"✅ Online" if bk_ok else "❌ Offline"}</div></div>',unsafe_allow_html=True)
    with c3:
        f=lt_file() or ""
        st.markdown(f'<div class="metric-mini"><div class="m-label">Logitrein</div><div class="m-val" style="color:#7a9bbf;font-size:.9rem">{get_size(f) if f else "—"}</div></div>',unsafe_allow_html=True)
    with c4:
        f=banco_file() or ""
        st.markdown(f'<div class="metric-mini"><div class="m-label">Banco</div><div class="m-val" style="color:#7a9bbf;font-size:.9rem">{get_size(f) if f else "—"}</div></div>',unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_a,col_b = st.columns(2, gap="large")

    with col_a:
        st.markdown("""<div class="app-card">
            <div class="card-title">🏭 Logitrein v12 <span class="badge b-blue">Logística</span></div>
            <div class="card-desc">Sistema de gestão operacional. Controle de equipes, ponto eletrônico,
            DP com folha de pagamento e integração bancária automática.</div>
            <div class="card-hint">Acesse com suas credenciais fornecidas pelo coordenador.</div>
        </div>""", unsafe_allow_html=True)
        if lt_ok:
            url = html_to_b64(lt_file())
            st.markdown(f'<a href="{url}" target="_blank" style="text-decoration:none"><div style="background:#1a56db;color:#fff;border-radius:8px;padding:11px;text-align:center;font-family:Syne,sans-serif;font-weight:700;font-size:.88rem;cursor:pointer">🚀 Abrir Logitrein v12</div></a>', unsafe_allow_html=True)
        else:
            st.button("🚀 Abrir Logitrein v12", disabled=True, use_container_width=True)

    with col_b:
        st.markdown("""<div class="app-card">
            <div class="card-title">🏦 Banco Logitrein <span class="badge b-teal">Financeiro</span></div>
            <div class="card-desc">Banco digital completo. Conta corrente, Pix, transferências,
            investimentos, crédito e depósito automático de salários via folha.</div>
            <div class="card-hint">Acesse com suas credenciais fornecidas pelo gerente da agência.</div>
        </div>""", unsafe_allow_html=True)
        if bk_ok:
            url = html_to_b64(banco_file())
            st.markdown(f'<a href="{url}" target="_blank" style="text-decoration:none"><div style="background:#00c9a7;color:#09182e;border-radius:8px;padding:11px;text-align:center;font-family:Syne,sans-serif;font-weight:700;font-size:.88rem;cursor:pointer">🏦 Abrir Banco Logitrein</div></a>', unsafe_allow_html=True)
        else:
            st.button("🏦 Abrir Banco Logitrein", disabled=True, use_container_width=True)

    st.markdown("""
    <div class="info-box" style="margin-top:16px">
        🔗 <strong>Integração automática:</strong> Ao fechar a folha no Logitrein,
        os salários são depositados nas contas do Banco Logitrein.
    </div>
    <div class="warn-box">
        💡 Os sistemas abrem em <strong>nova aba</strong> para garantir o funcionamento correto do login.
    </div>""", unsafe_allow_html=True)

# ADMIN
def pagina_admin():
    if st.button("← Voltar", key="back_adm"):
        st.session_state.pagina='portal'; st.session_state.admin_ok=False; st.rerun()

    if not st.session_state.admin_ok:
        st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
        _,col_c,_ = st.columns([1,1.6,1])
        with col_c:
            st.markdown("""<div style="background:#0f1929;border:1px solid rgba(245,200,66,.2);
            border-radius:14px;padding:32px 28px;text-align:center">
            <div style="font-size:2rem;margin-bottom:8px">🔐</div>
            <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;color:#f5c842;margin-bottom:4px">Área Restrita</div>
            <div style="font-size:.75rem;color:#3a5070;margin-bottom:20px">Acesso exclusivo ao proprietário.</div>
            </div>""", unsafe_allow_html=True)
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            senha = st.text_input("", type="password", placeholder="Senha de administrador", label_visibility="collapsed")
            if st.button("🔓 Entrar", use_container_width=True):
                if checar_admin(senha):
                    st.session_state.admin_ok=True; st.rerun()
                else:
                    st.error("❌ Acesso negado.")
        return

    st.markdown("""<div style="display:flex;align-items:center;gap:12px;margin-bottom:24px;
    padding:16px 20px;background:#0f1929;border:1px solid rgba(245,200,66,.2);border-radius:12px">
    <div style="font-size:1.3rem">⚙️</div>
    <div><div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:800;color:#f5c842">
    Painel Administrativo</div>
    <div style="font-size:.73rem;color:#5a7090">Jorge Zensque — Proprietário · Sessão ativa</div>
    </div></div>""", unsafe_allow_html=True)

    tab1,tab2,tab3 = st.tabs(["📁 Arquivos HTML","📊 Status","🔑 Segurança"])

    with tab1:
        st.caption("Upload de versões novas sem acessar o GitHub.")
        c1,c2 = st.columns(2)
        with c1:
            f=lt_file() or 'logitrein.html'
            st.markdown(f"**🏭 Logitrein** — `{f}`")
            st.caption(f"{'✅ '+get_size(f) if file_exists(f) else '❌ Não encontrado'}")
            up=st.file_uploader("Novo Logitrein HTML",type=['html'],key='up_lt')
            if up:
                (Path(__file__).parent/'logitrein.html').write_bytes(up.read())
                st.success("✅ Atualizado!"); st.rerun()
        with c2:
            f=banco_file() or 'logitrein_banco_v2.html'
            st.markdown(f"**🏦 Banco** — `{f}`")
            st.caption(f"{'✅ '+get_size(f) if file_exists(f) else '❌ Não encontrado'}")
            up=st.file_uploader("Novo Banco HTML",type=['html'],key='up_bk')
            if up:
                (Path(__file__).parent/'logitrein_banco_v2.html').write_bytes(up.read())
                st.success("✅ Atualizado!"); st.rerun()

    with tab2:
        for fname,label in [('logitrein.html','🏭 Logitrein'),('logitrein_banco_v2.html','🏦 Banco'),('app.py','⚙️ Portal'),('requirements.txt','📦 Requirements')]:
            ok=file_exists(fname); cor='#22c55e' if ok else '#e94b4b'
            st.markdown(f"<div style='display:flex;justify-content:space-between;padding:8px 12px;background:rgba(255,255,255,.03);border-radius:8px;margin-bottom:5px;font-size:.82rem'><span style='color:#c0d4e8'>{label}</span><span style='color:{cor}'>{'✅ '+get_size(fname) if ok else '❌ Ausente'}</span></div>",unsafe_allow_html=True)
        st.caption(f"Verificado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

    with tab3:
        st.markdown("##### Alterar senha de administrador")
        n1=st.text_input("Nova senha",type="password",placeholder="Mínimo 8 caracteres")
        n2=st.text_input("Confirmar",type="password",placeholder="Repita")
        if st.button("🔑 Gerar hash"):
            if len(n1)<8: st.error("Mínimo 8 caracteres.")
            elif n1!=n2: st.error("Senhas não conferem.")
            else:
                h=hashlib.sha256(n1.encode()).hexdigest()
                st.success("✅ Cole no app.py:")
                st.code(f'ADMIN_HASH = "{h}"', language="python")
        st.divider()
        if st.button("🚪 Sair da área admin"):
            st.session_state.admin_ok=False; st.session_state.pagina='portal'; st.rerun()

# ROTEADOR
if st.session_state.pagina=='admin': pagina_admin()
else: pagina_portal()
