"""
Logitrein + Banco — Portal de Acesso
Streamlit v2.1 — Seguro, sem senhas expostas
"""
import streamlit as st
import base64
import hashlib
from pathlib import Path
from datetime import datetime

# ──────────────────────────────────────────────────────────
#  CONFIGURAÇÃO
# ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Logitrein — Portal",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ──────────────────────────────────────────────────────────
#  SENHA ADMIN — hash SHA-256 da senha do proprietário
#  Senha: jorge2026master
#  Para alterar: python3 -c "import hashlib; print(hashlib.sha256('NOVA_SENHA'.encode()).hexdigest())"
# ──────────────────────────────────────────────────────────
ADMIN_HASH = hashlib.sha256("jorge2026master".encode()).hexdigest()

def checar_admin(senha_digitada: str) -> bool:
    return hashlib.sha256(senha_digitada.encode()).hexdigest() == ADMIN_HASH

# ──────────────────────────────────────────────────────────
#  CSS
# ──────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background: #09182e !important;
    color: #ddeaf8 !important;
}
.main, section[data-testid="stMain"] { background: #09182e !important; }
.block-container { padding: 2rem 2rem 1rem !important; max-width: 1100px; }
h1,h2,h3 { font-family: 'Syne', sans-serif !important; }
.banner {
    background: linear-gradient(135deg,#112240,#0d2a55);
    border: 1px solid rgba(0,201,167,.15);
    border-radius: 16px; padding: 32px 36px; margin-bottom: 24px;
}
.brand { font-family:'Syne',sans-serif; font-size:2rem; font-weight:800; color:#00c9a7; }
.brand span { color:#f5c842; }
.sub { font-size:.9rem; color:#7a9bbf; margin-top:4px; }
.app-card {
    background: #132240; border: 1px solid rgba(255,255,255,.07);
    border-radius: 14px; padding: 26px 22px; margin-bottom: 14px;
    min-height: 160px;
}
.card-title { font-family:'Syne',sans-serif; font-size:1.05rem; font-weight:700; color:#fff; margin-bottom:8px; }
.card-desc { font-size:.82rem; color:#7a9bbf; line-height:1.6; }
.card-hint { font-size:.72rem; color:#3a5070; margin-top:10px; }
.badge { display:inline-block; padding:2px 9px; border-radius:99px; font-size:.58rem; font-weight:700; text-transform:uppercase; letter-spacing:.8px; margin-left:6px; }
.b-teal { background:rgba(0,201,167,.14); color:#00c9a7; }
.b-blue { background:rgba(26,86,219,.2); color:#93b4f7; }
.b-gold { background:rgba(245,200,66,.15); color:#f5c842; }
.metric-mini { background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.07); border-radius:10px; padding:12px; text-align:center; }
.m-label { font-size:.6rem; color:#7a9bbf; text-transform:uppercase; letter-spacing:.8px; }
.m-val { font-family:'Syne',sans-serif; font-size:1.1rem; font-weight:700; }
.info-box { background:rgba(0,201,167,.07); border:1px solid rgba(0,201,167,.18); border-radius:10px; padding:12px 16px; font-size:.8rem; color:#6ee7da; margin:10px 0; line-height:1.6; }
#MainMenu,footer,header,.stDeployButton { visibility:hidden; display:none !important; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────
#  HELPERS
# ──────────────────────────────────────────────────────────
def file_exists(f): return (Path(__file__).parent / f).exists()

def get_size(f):
    p = Path(__file__).parent / f
    if not p.exists(): return "—"
    s = p.stat().st_size
    return f"{s/1024/1024:.1f} MB" if s > 1024*1024 else f"{s/1024:.0f} KB"

def html_to_b64(filename):
    p = Path(__file__).parent / filename
    if not p.exists(): return None
    b64 = base64.b64encode(p.read_bytes()).decode()
    return f"data:text/html;base64,{b64}"

def lt_file():
    for f in ['logitrein.html', 'logitrein_v12_integrado.html']:
        if file_exists(f): return f
    return None

def banco_file():
    for f in ['logitrein_banco_v2.html', 'banco.html']:
        if file_exists(f): return f
    return None

# ──────────────────────────────────────────────────────────
#  ESTADO DA SESSÃO
# ──────────────────────────────────────────────────────────
for k, v in [('pagina', 'portal'), ('admin_ok', False)]:
    if k not in st.session_state:
        st.session_state[k] = v

# ──────────────────────────────────────────────────────────
#  SIDEBAR — limpa, sem nenhuma senha ou dado sensível
# ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:800;color:#00c9a7;
    padding:8px 0 14px;border-bottom:1px solid rgba(255,255,255,.07);margin-bottom:12px">
        🏦 Logitrein Portal
    </div>""", unsafe_allow_html=True)

    if st.button("🏠 Portal", use_container_width=True):
        st.session_state.pagina = 'portal'
        st.rerun()

    if st.button("🏭 Logitrein v12", use_container_width=True, disabled=lt_file() is None):
        st.session_state.pagina = 'logitrein'
        st.rerun()

    if st.button("🏦 Banco Logitrein", use_container_width=True, disabled=banco_file() is None):
        st.session_state.pagina = 'banco'
        st.rerun()

    st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

    # Botão admin discreto — só um ícone, sem texto que chame atenção
    if st.button("⚙️", key="btn_admin_sb", help="Administração do sistema"):
        st.session_state.pagina = 'admin'
        st.rerun()

    st.markdown(
        f"<div style='font-size:.6rem;color:#1e2d45;padding-top:16px'>"
        f"v2.1 · {datetime.now().strftime('%d/%m/%Y')}</div>",
        unsafe_allow_html=True
    )

# ──────────────────────────────────────────────────────────
#  PORTAL PRINCIPAL
# ──────────────────────────────────────────────────────────
def pagina_portal():
    st.markdown("""
    <div class="banner">
        <div class="brand">🏭 Logit<span>rein</span> · 🏦 Banco</div>
        <div class="sub">Portal integrado de gestão logística e financeira · Palmas/TO</div>
    </div>""", unsafe_allow_html=True)

    lt_ok = lt_file() is not None
    bk_ok = banco_file() is not None

    c1, c2, c3, c4 = st.columns(4)
    for col, label, ok, size_f in [
        (c1, "Logitrein v12", lt_ok, lt_file() or ""),
        (c2, "Banco Logitrein", bk_ok, banco_file() or ""),
        (c3, "Tamanho LT", lt_ok, lt_file() or ""),
        (c4, "Tamanho Banco", bk_ok, banco_file() or ""),
    ]:
        with col:
            if label.startswith("Tamanho"):
                nm = label.replace("Tamanho ", "")
                st.markdown(f'<div class="metric-mini"><div class="m-label">{nm}</div>'
                            f'<div class="m-val" style="color:#7a9bbf;font-size:.9rem">'
                            f'{get_size(size_f) if size_f else "—"}</div></div>', unsafe_allow_html=True)
            else:
                cor = '#22c55e' if ok else '#e94b4b'
                st.markdown(f'<div class="metric-mini"><div class="m-label">{label}</div>'
                            f'<div class="m-val" style="color:{cor}">{"✅ Online" if ok else "❌ Offline"}</div></div>',
                            unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2, gap="large")
    with col_a:
        st.markdown("""
        <div class="app-card">
            <div class="card-title">🏭 Logitrein v12 <span class="badge b-blue">Logística</span></div>
            <div class="card-desc">Sistema de gestão operacional. Controle de equipes, ponto eletrônico,
            DP com folha de pagamento e integração bancária automática.</div>
            <div class="card-hint">Acesse com suas credenciais fornecidas pelo coordenador.</div>
        </div>""", unsafe_allow_html=True)
        if st.button("🚀 Abrir Logitrein v12", key="btn_lt", use_container_width=True, disabled=not lt_ok):
            st.session_state.pagina = 'logitrein'
            st.rerun()

    with col_b:
        st.markdown("""
        <div class="app-card">
            <div class="card-title">🏦 Banco Logitrein <span class="badge b-teal">Financeiro</span></div>
            <div class="card-desc">Banco digital completo. Conta corrente, Pix, transferências,
            investimentos, crédito e depósito automático de salários via folha.</div>
            <div class="card-hint">Acesse com suas credenciais fornecidas pelo gerente da agência.</div>
        </div>""", unsafe_allow_html=True)
        if st.button("🏦 Abrir Banco Logitrein", key="btn_banco", use_container_width=True, disabled=not bk_ok):
            st.session_state.pagina = 'banco'
            st.rerun()

    st.markdown("""
    <div class="info-box" style="margin-top:14px">
        🔗 <strong>Integração automática:</strong> Ao fechar a folha no Logitrein,
        os salários líquidos são depositados automaticamente nas contas do Banco Logitrein.
    </div>""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────
#  LOGITREIN
# ──────────────────────────────────────────────────────────
def pagina_logitrein():
    col_back, col_title = st.columns([1, 6])
    with col_back:
        if st.button("← Voltar", key="back_lt"):
            st.session_state.pagina = 'portal'; st.rerun()
    with col_title:
        st.markdown("<h2 style='margin:0;font-family:Syne,sans-serif;color:#38bdf8'>🏭 Logitrein v12</h2>",
                    unsafe_allow_html=True)
    f = lt_file()
    if not f:
        st.error("Arquivo não encontrado. Contate o administrador.")
        return
    data_url = html_to_b64(f)
    st.markdown(f'<div style="border:1px solid rgba(255,255,255,.07);border-radius:14px;overflow:hidden">'
                f'<iframe src="{data_url}" width="100%" height="920" frameborder="0" style="display:block">'
                f'</iframe></div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────
#  BANCO
# ──────────────────────────────────────────────────────────
def pagina_banco():
    col_back, col_title = st.columns([1, 6])
    with col_back:
        if st.button("← Voltar", key="back_banco"):
            st.session_state.pagina = 'portal'; st.rerun()
    with col_title:
        st.markdown("<h2 style='margin:0;font-family:Syne,sans-serif;color:#00c9a7'>🏦 Banco Logitrein</h2>",
                    unsafe_allow_html=True)
    f = banco_file()
    if not f:
        st.error("Arquivo não encontrado. Contate o administrador.")
        return
    data_url = html_to_b64(f)
    st.markdown(f'<div style="border:1px solid rgba(255,255,255,.07);border-radius:14px;overflow:hidden">'
                f'<iframe src="{data_url}" width="100%" height="920" frameborder="0" style="display:block">'
                f'</iframe></div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────
#  ÁREA ADMIN — protegida por senha (somente Jorge Zensque)
# ──────────────────────────────────────────────────────────
def pagina_admin():
    if st.button("← Voltar ao Portal", key="back_adm"):
        st.session_state.pagina = 'portal'
        st.session_state.admin_ok = False
        st.rerun()

    # ── Tela de login admin ──
    if not st.session_state.admin_ok:
        st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
        _, col_c, _ = st.columns([1, 1.6, 1])
        with col_c:
            st.markdown("""
            <div style="background:#0f1929;border:1px solid rgba(245,200,66,.2);border-radius:14px;
            padding:32px 28px;text-align:center">
                <div style="font-size:2rem;margin-bottom:8px">🔐</div>
                <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;
                color:#f5c842;margin-bottom:4px">Área Restrita</div>
                <div style="font-size:.75rem;color:#3a5070;margin-bottom:20px">
                    Acesso exclusivo ao proprietário do sistema.
                </div>
            </div>""", unsafe_allow_html=True)
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            senha = st.text_input("", type="password", placeholder="Senha de administrador",
                                  label_visibility="collapsed")
            if st.button("🔓 Entrar", use_container_width=True):
                if checar_admin(senha):
                    st.session_state.admin_ok = True
                    st.rerun()
                else:
                    st.error("❌ Acesso negado.")
        return

    # ── Painel admin autenticado ──
    st.markdown("""
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:24px;
    padding:16px 20px;background:#0f1929;border:1px solid rgba(245,200,66,.2);border-radius:12px">
        <div style="font-size:1.4rem">⚙️</div>
        <div>
            <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:800;color:#f5c842">
                Painel Administrativo
            </div>
            <div style="font-size:.73rem;color:#5a7090">
                Jorge Zensque — Proprietário · Sessão ativa
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📁 Arquivos HTML", "📊 Status do Sistema", "🔑 Segurança"])

    with tab1:
        st.markdown("##### Atualizar arquivos sem precisar acessar o GitHub")
        st.caption("⚠️ O upload substitui permanentemente o arquivo no servidor.")
        col1, col2 = st.columns(2)

        with col1:
            f = lt_file() or 'logitrein.html'
            st.markdown(f"**🏭 Logitrein v12** — `{f}`")
            st.caption(f"{'✅ ' + get_size(f) if file_exists(f) else '❌ Não encontrado'}")
            up = st.file_uploader("Novo arquivo Logitrein", type=['html'], key='up_lt')
            if up:
                dest = Path(__file__).parent / 'logitrein.html'
                dest.write_bytes(up.read())
                st.success("✅ logitrein.html atualizado!")
                st.rerun()

        with col2:
            f = banco_file() or 'logitrein_banco_v2.html'
            st.markdown(f"**🏦 Banco** — `{f}`")
            st.caption(f"{'✅ ' + get_size(f) if file_exists(f) else '❌ Não encontrado'}")
            up = st.file_uploader("Novo arquivo Banco", type=['html'], key='up_bk')
            if up:
                dest = Path(__file__).parent / 'logitrein_banco_v2.html'
                dest.write_bytes(up.read())
                st.success("✅ logitrein_banco_v2.html atualizado!")
                st.rerun()

    with tab2:
        st.markdown("##### Arquivos no servidor")
        for fname, label in [
            ('logitrein.html', '🏭 Logitrein v12'),
            ('logitrein_banco_v2.html', '🏦 Banco Logitrein'),
            ('app.py', '⚙️ Portal Streamlit'),
            ('requirements.txt', '📦 Requirements'),
        ]:
            ok = file_exists(fname)
            cor = '#22c55e' if ok else '#e94b4b'
            st.markdown(
                f"<div style='display:flex;justify-content:space-between;align-items:center;"
                f"padding:9px 14px;background:rgba(255,255,255,.03);border-radius:8px;margin-bottom:5px;font-size:.82rem'>"
                f"<span style='color:#c0d4e8'>{label} <code style='font-size:.7rem;color:#5a7090'>{fname}</code></span>"
                f"<span style='color:{cor};font-weight:600'>{'✅ ' + get_size(fname) if ok else '❌ Ausente'}</span></div>",
                unsafe_allow_html=True)
        st.caption(f"Verificado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}")

    with tab3:
        st.markdown("##### Alterar senha de administrador")
        st.caption("Após alterar, copie o hash gerado e atualize o `app.py` no GitHub na linha `ADMIN_HASH`.")
        nova1 = st.text_input("Nova senha", type="password", placeholder="Mínimo 8 caracteres")
        nova2 = st.text_input("Confirmar", type="password", placeholder="Repita a senha")
        if st.button("🔑 Gerar novo hash"):
            if len(nova1) < 8:
                st.error("Senha muito curta — mínimo 8 caracteres.")
            elif nova1 != nova2:
                st.error("As senhas não conferem.")
            else:
                novo_hash = hashlib.sha256(nova1.encode()).hexdigest()
                st.success("✅ Hash gerado! Copie e cole no app.py:")
                st.code(f'ADMIN_HASH = "{novo_hash}"', language="python")

        st.divider()
        if st.button("🚪 Encerrar sessão admin", type="secondary"):
            st.session_state.admin_ok = False
            st.session_state.pagina = 'portal'
            st.rerun()


# ──────────────────────────────────────────────────────────
#  ROTEADOR
# ──────────────────────────────────────────────────────────
p = st.session_state.pagina
if p == 'logitrein':    pagina_logitrein()
elif p == 'banco':      pagina_banco()
elif p == 'admin':      pagina_admin()
else:                   pagina_portal()
