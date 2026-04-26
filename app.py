"""
Logitrein Portal v6.0 — arquivo único, sem switch_page, sem pages/
"""
import streamlit as st
import hashlib
from pathlib import Path
from datetime import datetime

# ── Senha admin ──
ADMIN_HASH = hashlib.sha256("jorge2026master".encode()).hexdigest()
def checar_admin(s): return hashlib.sha256(s.encode()).hexdigest() == ADMIN_HASH

def file_exists(f): return (Path(__file__).parent / f).exists()
def get_size(f):
    p = Path(__file__).parent / f
    if not p.exists(): return "—"
    s = p.stat().st_size
    return f"{s/1024/1024:.1f} MB" if s>1024*1024 else f"{s/1024:.0f} KB"
def lt_file():
    for f in ['logitrein.html','logitrein_v12_integrado.html']:
        if file_exists(f): return f
    return None
def banco_file():
    for f in ['logitrein_banco_v2.html','banco.html']:
        if file_exists(f): return f
    return None

st.set_page_config(page_title="Logitrein — Portal", page_icon="🏦", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif!important;background:#09182e!important;color:#ddeaf8!important}
.main,section[data-testid="stMain"]{background:#09182e!important}
.block-container{padding:1.5rem 2rem!important;max-width:1100px}
.banner{background:linear-gradient(135deg,#112240,#0d2a55);border:1px solid rgba(0,201,167,.15);border-radius:16px;padding:28px 32px;margin-bottom:20px}
.brand{font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;color:#00c9a7}
.brand span{color:#f5c842}
.sub{font-size:.85rem;color:#7a9bbf;margin-top:4px}
.card{background:#132240;border:1px solid rgba(255,255,255,.07);border-radius:14px;padding:22px 20px;margin-bottom:12px;min-height:155px}
.ct{font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:#fff;margin-bottom:8px}
.cd{font-size:.81rem;color:#7a9bbf;line-height:1.6}
.ch{font-size:.7rem;color:#2a4060;margin-top:8px}
.badge{display:inline-block;padding:2px 8px;border-radius:99px;font-size:.55rem;font-weight:700;text-transform:uppercase;letter-spacing:.8px;margin-left:6px}
.bt{background:rgba(0,201,167,.14);color:#00c9a7}
.bb{background:rgba(26,86,219,.2);color:#93b4f7}
.mm{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.07);border-radius:10px;padding:12px;text-align:center}
.ml{font-size:.58rem;color:#7a9bbf;text-transform:uppercase;letter-spacing:.8px}
.mv{font-family:'Syne',sans-serif;font-size:1.05rem;font-weight:700}
.ib{background:rgba(0,201,167,.07);border:1px solid rgba(0,201,167,.18);border-radius:10px;padding:12px 16px;font-size:.79rem;color:#6ee7da;margin-top:12px;line-height:1.6}
/* remove streamlit chrome */
#MainMenu,footer,header,.stDeployButton{visibility:hidden!important;display:none!important}
/* sidebar */
section[data-testid="stSidebar"]{background:#112240!important}
</style>
""", unsafe_allow_html=True)

# ── estado ──
if 'tela' not in st.session_state: st.session_state.tela = 'portal'
if 'admin_ok' not in st.session_state: st.session_state.admin_ok = False

# ── sidebar ──
with st.sidebar:
    st.markdown("<div style='font-family:Syne,sans-serif;font-size:.95rem;font-weight:800;color:#00c9a7;padding:6px 0 12px;border-bottom:1px solid rgba(255,255,255,.07);margin-bottom:10px'>🏦 Logitrein Portal</div>", unsafe_allow_html=True)
    if st.button("🏠 Portal", use_container_width=True):
        st.session_state.tela = 'portal'; st.rerun()
    if st.button("🏭 Logitrein v12", use_container_width=True, disabled=lt_file() is None):
        st.session_state.tela = 'logitrein'; st.rerun()
    if st.button("🏦 Banco Logitrein", use_container_width=True, disabled=banco_file() is None):
        st.session_state.tela = 'banco'; st.rerun()
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    if st.button("⚙️ Admin", use_container_width=False):
        st.session_state.tela = 'admin'; st.rerun()
    st.markdown(f"<div style='font-size:.6rem;color:#1e2d45;margin-top:14px'>v6.0 · {datetime.now().strftime('%d/%m/%Y')}</div>", unsafe_allow_html=True)

# ════════════════════════════════════
tela = st.session_state.tela

# ── PORTAL ──────────────────────────
if tela == 'portal':
    lt_ok = lt_file() is not None
    bk_ok = banco_file() is not None

    st.markdown("""<div class="banner">
        <div class="brand">🏭 Logit<span>rein</span> · 🏦 Banco</div>
        <div class="sub">Portal integrado de gestão logística e financeira · Palmas/TO</div>
    </div>""", unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    with c1:
        cor='#22c55e' if lt_ok else '#e94b4b'
        st.markdown(f'<div class="mm"><div class="ml">Logitrein v12</div><div class="mv" style="color:{cor}">{"✅ Online" if lt_ok else "❌ Offline"}</div></div>',unsafe_allow_html=True)
    with c2:
        cor='#22c55e' if bk_ok else '#e94b4b'
        st.markdown(f'<div class="mm"><div class="ml">Banco Logitrein</div><div class="mv" style="color:{cor}">{"✅ Online" if bk_ok else "❌ Offline"}</div></div>',unsafe_allow_html=True)
    with c3:
        f=lt_file() or ""
        st.markdown(f'<div class="mm"><div class="ml">Logitrein</div><div class="mv" style="color:#7a9bbf;font-size:.9rem">{get_size(f) if f else "—"}</div></div>',unsafe_allow_html=True)
    with c4:
        f=banco_file() or ""
        st.markdown(f'<div class="mm"><div class="ml">Banco</div><div class="mv" style="color:#7a9bbf;font-size:.9rem">{get_size(f) if f else "—"}</div></div>',unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    ca, cb = st.columns(2, gap="large")

    with ca:
        st.markdown("""<div class="card">
            <div class="ct">🏭 Logitrein v12 <span class="badge bb">Logística</span></div>
            <div class="cd">Sistema de gestão operacional. Controle de equipes, ponto eletrônico,
            DP com folha de pagamento e integração bancária automática.</div>
            <div class="ch">Acesse com suas credenciais fornecidas pelo coordenador.</div>
        </div>""", unsafe_allow_html=True)
        if st.button("🚀 Abrir Logitrein v12", use_container_width=True, disabled=not lt_ok):
            st.session_state.tela = 'logitrein'; st.rerun()

    with cb:
        st.markdown("""<div class="card">
            <div class="ct">🏦 Banco Logitrein <span class="badge bt">Financeiro</span></div>
            <div class="cd">Banco digital completo. Conta corrente, Pix, transferências,
            investimentos, crédito e depósito automático de salários via folha.</div>
            <div class="ch">Acesse com suas credenciais fornecidas pelo gerente da agência.</div>
        </div>""", unsafe_allow_html=True)
        if st.button("🏦 Abrir Banco Logitrein", use_container_width=True, disabled=not bk_ok):
            st.session_state.tela = 'banco'; st.rerun()

    st.markdown('<div class="ib">🔗 <strong>Integração automática:</strong> Ao fechar a folha no Logitrein, os salários são depositados nas contas do Banco Logitrein.</div>', unsafe_allow_html=True)

# ── LOGITREIN ────────────────────────
elif tela == 'logitrein':
    f = lt_file()
    if f:
        p = Path(__file__).parent / f
        st.components.v1.html(p.read_text(encoding='utf-8'), height=950, scrolling=True)
    else:
        st.error("Arquivo logitrein.html não encontrado.")
        if st.button("← Voltar"): st.session_state.tela='portal'; st.rerun()

# ── BANCO ────────────────────────────
elif tela == 'banco':
    f = banco_file()
    if f:
        p = Path(__file__).parent / f
        st.components.v1.html(p.read_text(encoding='utf-8'), height=950, scrolling=True)
    else:
        st.error("Arquivo banco não encontrado.")
        if st.button("← Voltar"): st.session_state.tela='portal'; st.rerun()

# ── ADMIN ────────────────────────────
elif tela == 'admin':
    if not st.session_state.admin_ok:
        st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
        _, col, _ = st.columns([1, 1.4, 1])
        with col:
            st.markdown("""<div style="background:#0f1929;border:1px solid rgba(245,200,66,.2);
            border-radius:14px;padding:32px 28px;text-align:center">
            <div style="font-size:2rem;margin-bottom:8px">🔐</div>
            <div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;color:#f5c842;margin-bottom:6px">Área Restrita</div>
            <div style="font-size:.75rem;color:#3a5070;margin-bottom:20px">Acesso exclusivo ao proprietário.</div>
            </div>""", unsafe_allow_html=True)
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            senha = st.text_input("", type="password", placeholder="Senha de administrador", label_visibility="collapsed")
            if st.button("🔓 Entrar", use_container_width=True):
                if checar_admin(senha):
                    st.session_state.admin_ok = True; st.rerun()
                else:
                    st.error("❌ Acesso negado.")
    else:
        st.markdown("""<div style="padding:14px 18px;background:#0f1929;border:1px solid rgba(245,200,66,.2);
        border-radius:12px;margin-bottom:20px">
        <span style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;color:#f5c842">⚙️ Painel Administrativo</span>
        <span style="font-size:.72rem;color:#5a7090;margin-left:12px">Jorge Zensque — Proprietário · Sessão ativa</span>
        </div>""", unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs(["📁 Arquivos HTML", "📊 Status", "🔑 Segurança"])

        with tab1:
            st.caption("Upload de versões novas dos sistemas.")
            c1, c2 = st.columns(2)
            with c1:
                f = lt_file() or 'logitrein.html'
                st.markdown(f"**🏭 Logitrein** — `{f}`")
                st.caption(f"{'✅ ' + get_size(f) if file_exists(f) else '❌ Não encontrado'}")
                up = st.file_uploader("Novo Logitrein HTML", type=['html'], key='up_lt')
                if up:
                    (Path(__file__).parent / 'logitrein.html').write_bytes(up.read())
                    st.success("✅ Atualizado!"); st.rerun()
            with c2:
                f = banco_file() or 'logitrein_banco_v2.html'
                st.markdown(f"**🏦 Banco** — `{f}`")
                st.caption(f"{'✅ ' + get_size(f) if file_exists(f) else '❌ Não encontrado'}")
                up = st.file_uploader("Novo Banco HTML", type=['html'], key='up_bk')
                if up:
                    (Path(__file__).parent / 'logitrein_banco_v2.html').write_bytes(up.read())
                    st.success("✅ Atualizado!"); st.rerun()

        with tab2:
            for fn, lb in [('logitrein.html','🏭 Logitrein'),('logitrein_banco_v2.html','🏦 Banco'),('app.py','⚙️ Portal'),('requirements.txt','📦 Requirements')]:
                ok = file_exists(fn); cor = '#22c55e' if ok else '#e94b4b'
                st.markdown(f"<div style='display:flex;justify-content:space-between;padding:8px 12px;background:rgba(255,255,255,.03);border-radius:8px;margin-bottom:5px;font-size:.81rem'><span style='color:#c0d4e8'>{lb}</span><span style='color:{cor}'>{'✅ ' + get_size(fn) if ok else '❌ Ausente'}</span></div>", unsafe_allow_html=True)
            st.caption(f"Verificado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

        with tab3:
            st.markdown("##### Alterar senha de administrador")
            n1 = st.text_input("Nova senha", type="password", placeholder="Mínimo 8 caracteres")
            n2 = st.text_input("Confirmar", type="password", placeholder="Repita a senha")
            if st.button("🔑 Gerar hash"):
                if len(n1) < 8: st.error("Mínimo 8 caracteres.")
                elif n1 != n2: st.error("Senhas não conferem.")
                else:
                    h = hashlib.sha256(n1.encode()).hexdigest()
                    st.success("✅ Cole no app.py na linha ADMIN_HASH:")
                    st.code(f'ADMIN_HASH = "{h}"', language="python")
            st.divider()
            if st.button("🚪 Sair da área admin"):
                st.session_state.admin_ok = False
                st.session_state.tela = 'portal'
                st.rerun()
