"""
Logitrein Portal v5.0 — Multi-página nativa do Streamlit
Cada sistema tem sua própria URL, localStorage funciona perfeitamente
"""
import streamlit as st
import hashlib
from pathlib import Path
from datetime import datetime

# ─────────────────────────────────────
#  SENHA ADMIN (hash SHA-256)
#  Senha: jorge2026master
# ─────────────────────────────────────
ADMIN_HASH = hashlib.sha256("jorge2026master".encode()).hexdigest()
def checar_admin(s): return hashlib.sha256(s.encode()).hexdigest() == ADMIN_HASH

def file_exists(f): return (Path(__file__).parent / f).exists()
def get_size(f):
    p = Path(__file__).parent / f
    if not p.exists(): return "—"
    s = p.stat().st_size
    return f"{s/1024/1024:.1f} MB" if s > 1024*1024 else f"{s/1024:.0f} KB"
def lt_file():
    for f in ['logitrein.html','logitrein_v12_integrado.html']:
        if file_exists(f): return f
    return None
def banco_file():
    for f in ['logitrein_banco_v2.html','banco.html']:
        if file_exists(f): return f
    return None

# ─────────────────────────────────────
#  PÁGINAS
# ─────────────────────────────────────
def page_portal():
    st.set_page_config(page_title="Logitrein — Portal", page_icon="🏦", layout="wide")
    _css()
    lt_ok = lt_file() is not None
    bk_ok = banco_file() is not None

    st.markdown("""<div class="banner">
        <div class="brand">🏭 Logit<span>rein</span> · 🏦 Banco</div>
        <div class="sub">Portal integrado de gestão logística e financeira · Palmas/TO</div>
    </div>""", unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    for col,lbl,ok,fname in [(c1,"Logitrein v12",lt_ok,lt_file()),(c2,"Banco Logitrein",bk_ok,banco_file()),(c3,"Tamanho LT",lt_ok,lt_file()),(c4,"Tamanho Banco",bk_ok,banco_file())]:
        with col:
            if lbl.startswith("Tamanho"):
                st.markdown(f'<div class="mm"><div class="ml">{lbl.replace("Tamanho ","")}</div><div class="mv" style="color:#7a9bbf;font-size:.9rem">{get_size(fname) if fname else "—"}</div></div>',unsafe_allow_html=True)
            else:
                cor='#22c55e' if ok else '#e94b4b'
                st.markdown(f'<div class="mm"><div class="ml">{lbl}</div><div class="mv" style="color:{cor}">{"✅ Online" if ok else "❌ Offline"}</div></div>',unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    ca,cb = st.columns(2, gap="large")

    with ca:
        st.markdown("""<div class="card">
            <div class="ct">🏭 Logitrein v12 <span class="badge bb">Logística</span></div>
            <div class="cd">Sistema de gestão operacional. Controle de equipes, ponto eletrônico,
            DP com folha de pagamento e integração bancária automática.</div>
            <div class="ch">Acesse com suas credenciais fornecidas pelo coordenador.</div>
        </div>""", unsafe_allow_html=True)
        if st.button("🚀 Abrir Logitrein v12", use_container_width=True, disabled=not lt_ok):
            st.switch_page("pages/logitrein.py")

    with cb:
        st.markdown("""<div class="card">
            <div class="ct">🏦 Banco Logitrein <span class="badge bt">Financeiro</span></div>
            <div class="cd">Banco digital completo. Conta corrente, Pix, transferências,
            investimentos, crédito e depósito automático de salários via folha.</div>
            <div class="ch">Acesse com suas credenciais fornecidas pelo gerente da agência.</div>
        </div>""", unsafe_allow_html=True)
        if st.button("🏦 Abrir Banco Logitrein", use_container_width=True, disabled=not bk_ok):
            st.switch_page("pages/banco.py")

    st.markdown("""
    <div class="ib">🔗 <strong>Integração automática:</strong> Ao fechar a folha no Logitrein, os salários são depositados nas contas do Banco Logitrein.</div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        _sidebar()
        if st.button("⚙️ Admin", key="adm_btn"):
            st.switch_page("pages/admin.py")

def _css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif!important;background:#09182e!important;color:#ddeaf8!important}
.main,section[data-testid="stMain"]{background:#09182e!important}
.block-container{padding:1.5rem 2rem!important;max-width:1100px}
.banner{background:linear-gradient(135deg,#112240,#0d2a55);border:1px solid rgba(0,201,167,.15);border-radius:16px;padding:28px 32px;margin-bottom:20px}
.brand{font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;color:#00c9a7}
.brand span{color:#f5c842}.sub{font-size:.85rem;color:#7a9bbf;margin-top:4px}
.card{background:#132240;border:1px solid rgba(255,255,255,.07);border-radius:14px;padding:22px 20px;margin-bottom:12px;min-height:160px}
.ct{font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:#fff;margin-bottom:8px}
.cd{font-size:.81rem;color:#7a9bbf;line-height:1.6}.ch{font-size:.7rem;color:#2a4060;margin-top:8px}
.badge{display:inline-block;padding:2px 8px;border-radius:99px;font-size:.55rem;font-weight:700;text-transform:uppercase;letter-spacing:.8px;margin-left:6px}
.bt{background:rgba(0,201,167,.14);color:#00c9a7}.bb{background:rgba(26,86,219,.2);color:#93b4f7}
.mm{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.07);border-radius:10px;padding:12px;text-align:center}
.ml{font-size:.58rem;color:#7a9bbf;text-transform:uppercase;letter-spacing:.8px}
.mv{font-family:'Syne',sans-serif;font-size:1.05rem;font-weight:700}
.ib{background:rgba(0,201,167,.07);border:1px solid rgba(0,201,167,.18);border-radius:10px;padding:12px 16px;font-size:.79rem;color:#6ee7da;margin-top:12px;line-height:1.6}
#MainMenu,footer,header,.stDeployButton{visibility:hidden!important;display:none!important}
</style>""", unsafe_allow_html=True)

def _sidebar():
    st.markdown("""<div style="font-family:'Syne',sans-serif;font-size:.95rem;font-weight:800;
    color:#00c9a7;padding:6px 0 12px;border-bottom:1px solid rgba(255,255,255,.07);margin-bottom:10px">
    🏦 Logitrein Portal</div>""", unsafe_allow_html=True)
    if st.button("🏠 Portal", use_container_width=True, key="sb_portal"):
        st.switch_page("app.py")
    if st.button("🏭 Logitrein v12", use_container_width=True, key="sb_lt", disabled=lt_file() is None):
        st.switch_page("pages/logitrein.py")
    if st.button("🏦 Banco Logitrein", use_container_width=True, key="sb_banco", disabled=banco_file() is None):
        st.switch_page("pages/banco.py")
    st.markdown(f"<div style='font-size:.6rem;color:#1e2d45;padding-top:14px'>v5.0 · {datetime.now().strftime('%d/%m/%Y')}</div>", unsafe_allow_html=True)

page_portal()
