"""
Logitrein Portal v8.0 — 100% Python/Streamlit (sem localStorage, sem HTML externo para o banco)
"""
import streamlit as st
import hashlib
import json
import random
import string
from pathlib import Path
from datetime import datetime

# ──────────────────────────────────────────────
#  CONFIGURAÇÃO DA PÁGINA (deve ser a 1ª chamada)
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Logitrein — Portal",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────
#  ADMIN
# ──────────────────────────────────────────────
ADMIN_HASH = hashlib.sha256("jorge2026master".encode()).hexdigest()

def checar_admin(s):
    return hashlib.sha256(s.encode()).hexdigest() == ADMIN_HASH

# ──────────────────────────────────────────────
#  UTILITÁRIOS DE ARQUIVO (Logitrein HTML)
# ──────────────────────────────────────────────
def file_exists(f):
    return (Path(__file__).parent / f).exists()

def get_size(f):
    p = Path(__file__).parent / f
    if not p.exists():
        return "—"
    s = p.stat().st_size
    return f"{s/1024/1024:.1f} MB" if s > 1024*1024 else f"{s/1024:.0f} KB"

def lt_file():
    for f in ['logitrein.html', 'logitrein_v12_integrado.html']:
        if file_exists(f):
            return f
    return None

# ──────────────────────────────────────────────
#  DADOS PADRÃO DO BANCO
# ──────────────────────────────────────────────
USUARIOS_PADRAO = [
    {
        "id": "u0", "login": "ceo", "senha": "ceo123",
        "nome": "Roberto Logitrein", "role": "ceo",
        "agencia": "0001", "conta": "00001-0", "saldo": 50000.0,
        "poupanca": 0, "investimentos": 0, "cashback": 0, "dividas": 0,
        "cartoes": [], "transacoes": [], "ativo": True
    },
    {
        "id": "u1", "login": "gerente1", "senha": "ger123",
        "nome": "Ana Gerente", "role": "gerente",
        "agencia": "0001", "conta": "00002-1", "saldo": 15000.0,
        "poupanca": 0, "investimentos": 0, "cashback": 0, "dividas": 0,
        "cartoes": [], "transacoes": [], "ativo": True
    },
    {
        "id": "u2", "login": "joao.silva", "senha": "123456",
        "nome": "João da Silva", "role": "pf",
        "agencia": "0001", "conta": "10001-2", "saldo": 3500.0,
        "poupanca": 500, "investimentos": 0, "cashback": 0, "dividas": 0,
        "cartoes": [], "transacoes": [], "ativo": True
    },
    {
        "id": "u3", "login": "emp.ltda", "senha": "empresa1",
        "nome": "Empresa Logitrein", "role": "pj",
        "agencia": "0001", "conta": "20001-3", "saldo": 25000.0,
        "poupanca": 0, "investimentos": 0, "cashback": 0, "dividas": 0,
        "cartoes": [], "transacoes": [], "ativo": True
    },
    {
        "id": "u4", "login": "maria.santos", "senha": "salario1",
        "nome": "Maria dos Santos", "role": "salario",
        "agencia": "0001", "conta": "30001-4", "saldo": 2800.0,
        "poupanca": 0, "investimentos": 0, "cashback": 0, "dividas": 0,
        "cartoes": [], "transacoes": [], "ativo": True,
        "empregador": "Empresa Logitrein"
    },
]

ROLE_LABELS = {
    "ceo": "CEO",
    "gerente": "Gerente",
    "pf": "Pessoa Física",
    "pj": "Pessoa Jurídica",
    "salario": "Conta Salário"
}
ROLE_CORES = {
    "ceo": "#f5c842",
    "gerente": "#93b4f7",
    "pf": "#00c9a7",
    "pj": "#fdba74",
    "salario": "#86efac"
}

# ──────────────────────────────────────────────
#  BANCO — session_state (sem localStorage)
# ──────────────────────────────────────────────
def init_banco():
    if 'banco_users' not in st.session_state:
        st.session_state.banco_users = json.loads(json.dumps(USUARIOS_PADRAO))
    if 'banco_user_id' not in st.session_state:
        st.session_state.banco_user_id = None

def get_users():
    return st.session_state.banco_users

def save_users(u):
    st.session_state.banco_users = u

def get_me():
    uid = st.session_state.banco_user_id
    return next((u for u in get_users() if u['id'] == uid), None)

def fmt(v):
    return f"R$ {float(v or 0):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def ts():
    return datetime.now().strftime("%d/%m/%Y %H:%M")

def add_tx(uid, tipo, desc, valor, direcao):
    users = get_users()
    for u in users:
        if u['id'] == uid:
            u.setdefault('transacoes', []).insert(0, {
                "tipo": tipo, "desc": desc,
                "valor": float(valor), "dir": direcao, "ts": ts()
            })
    save_users(users)

def update_saldo(uid, delta):
    users = get_users()
    for u in users:
        if u['id'] == uid:
            u['saldo'] = float(u.get('saldo', 0)) + delta
    save_users(users)

# ──────────────────────────────────────────────
#  CSS GLOBAL
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500&display=swap');
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background: #09182e !important;
    color: #ddeaf8 !important;
}
.main, section[data-testid="stMain"] { background: #09182e !important; }
.block-container { padding: 1.5rem 2rem !important; max-width: 1100px; }
.banner {
    background: linear-gradient(135deg, #112240, #0d2a55);
    border: 1px solid rgba(0,201,167,.15);
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 18px;
}
.brand { font-family: 'Syne', sans-serif; font-size: 1.6rem; font-weight: 800; color: #00c9a7; }
.brand span { color: #f5c842; }
.card {
    background: #132240;
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 12px;
    padding: 18px;
}
.metric-box {
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 10px;
    padding: 14px;
    text-align: center;
    margin-bottom: 10px;
}
.metric-label { font-size: .6rem; color: #7a9bbf; text-transform: uppercase; letter-spacing: .8px; }
.metric-value { font-family: 'Syne', sans-serif; font-size: 1.3rem; font-weight: 700; }
.tx-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 0;
    border-bottom: 1px solid rgba(255,255,255,.05);
    font-size: .82rem;
}
.tx-item:last-child { border: none; }
.badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 99px;
    font-size: .58rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .6px;
}
#MainMenu, footer, header, .stDeployButton { visibility: hidden !important; display: none !important; }
section[data-testid="stSidebar"] { background: #112240 !important; }
.stTextInput input, .stNumberInput input, .stSelectbox select {
    background: rgba(255,255,255,.05) !important;
    border: 1px solid rgba(255,255,255,.1) !important;
    color: #e2ecf8 !important;
    border-radius: 8px !important;
}
/* Esconde label do radio quando vazio */
.stRadio > label { display: none; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
#  INICIALIZAÇÃO DE ESTADO
# ──────────────────────────────────────────────
init_banco()

for k, v in [('tela', 'portal'), ('admin_ok', False)]:
    if k not in st.session_state:
        st.session_state[k] = v

# ──────────────────────────────────────────────
#  SIDEBAR
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<div style='font-family:Syne,sans-serif;font-size:.9rem;font-weight:800;"
        "color:#00c9a7;padding:4px 0 10px;border-bottom:1px solid rgba(255,255,255,.07);"
        "margin-bottom:8px'>🏦 Logitrein Portal</div>",
        unsafe_allow_html=True
    )

    if st.button("🏠 Portal", use_container_width=True):
        st.session_state.tela = 'portal'
        st.rerun()

    lt = lt_file()
    if st.button("🏭 Logitrein v12", use_container_width=True, disabled=(lt is None)):
        st.session_state.tela = 'logitrein'
        st.rerun()

    if st.button("🏦 Banco Logitrein", use_container_width=True):
        st.session_state.tela = 'banco'
        st.rerun()

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    if st.button("⚙️ Admin", use_container_width=False):
        st.session_state.tela = 'admin'
        st.rerun()

    # Info do usuário logado no banco
    if st.session_state.banco_user_id:
        me_sb = get_me()
        if me_sb:
            st.markdown(
                f"<div style='margin-top:16px;padding:8px;background:rgba(0,201,167,.07);"
                f"border-radius:8px;font-size:.75rem'>"
                f"<div style='color:#00c9a7;font-weight:600'>{me_sb['nome'][:20]}</div>"
                f"<div style='color:#5a7090'>{ROLE_LABELS.get(me_sb['role'], '')} · {fmt(me_sb['saldo'])}</div></div>",
                unsafe_allow_html=True
            )
            if st.button("🚪 Sair do Banco", use_container_width=True):
                st.session_state.banco_user_id = None
                st.session_state.tela = 'banco'
                st.rerun()

    st.markdown(
        f"<div style='font-size:.58rem;color:#1e2d45;margin-top:12px'>"
        f"v8.0 · {datetime.now().strftime('%d/%m/%Y')}</div>",
        unsafe_allow_html=True
    )

# ──────────────────────────────────────────────
#  ROTEADOR PRINCIPAL
# ──────────────────────────────────────────────
tela = st.session_state.tela

# ══════════════════════════════════════════════
#  TELA: PORTAL
# ══════════════════════════════════════════════
if tela == 'portal':
    st.markdown(
        '<div class="banner"><div class="brand">🏭 Logit<span>rein</span> · 🏦 Banco</div>'
        '<div style="font-size:.85rem;color:#7a9bbf;margin-top:4px">Portal integrado · Palmas/TO</div></div>',
        unsafe_allow_html=True
    )
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown(
            '<div class="card">'
            '<div style="font-family:Syne,sans-serif;font-weight:700;font-size:1rem;color:#fff;margin-bottom:6px">🏭 Logitrein v12</div>'
            '<div style="font-size:.81rem;color:#7a9bbf;line-height:1.5">Gestão operacional, equipes, ponto e DP integrado.</div>'
            '<div style="font-size:.7rem;color:#2a4060;margin-top:8px">Acesse com credenciais do coordenador.</div>'
            '</div>',
            unsafe_allow_html=True
        )
        if st.button("🚀 Abrir Logitrein v12", use_container_width=True, disabled=(lt is None)):
            st.session_state.tela = 'logitrein'
            st.rerun()
        if lt is None:
            st.caption("⚠️ Arquivo logitrein.html não encontrado. Faça upload via Admin.")
    with c2:
        st.markdown(
            '<div class="card">'
            '<div style="font-family:Syne,sans-serif;font-weight:700;font-size:1rem;color:#fff;margin-bottom:6px">🏦 Banco Logitrein</div>'
            '<div style="font-size:.81rem;color:#7a9bbf;line-height:1.5">Conta corrente, Pix, transferências, crédito e investimentos.</div>'
            '<div style="font-size:.7rem;color:#2a4060;margin-top:8px">Acesse com credenciais do gerente.</div>'
            '</div>',
            unsafe_allow_html=True
        )
        if st.button("🏦 Abrir Banco Logitrein", use_container_width=True):
            st.session_state.tela = 'banco'
            st.rerun()

    st.markdown(
        '<div style="background:rgba(0,201,167,.07);border:1px solid rgba(0,201,167,.18);'
        'border-radius:10px;padding:12px 16px;font-size:.79rem;color:#6ee7da;margin-top:14px;line-height:1.6">'
        '🔗 <strong>Integração automática:</strong> Ao fechar a folha no Logitrein, os salários são depositados nas contas do Banco.</div>',
        unsafe_allow_html=True
    )

# ══════════════════════════════════════════════
#  TELA: LOGITREIN v12
# ══════════════════════════════════════════════
elif tela == 'logitrein':
    f = lt_file()
    if f:
        p = Path(__file__).parent / f
        st.components.v1.html(p.read_text(encoding='utf-8'), height=950, scrolling=True)
    else:
        st.error("❌ Arquivo Logitrein não encontrado. Faça upload via ⚙️ Admin.")
        if st.button("← Voltar ao Portal"):
            st.session_state.tela = 'portal'
            st.rerun()

# ══════════════════════════════════════════════
#  TELA: BANCO — 100% Python, sem localStorage
# ══════════════════════════════════════════════
elif tela == 'banco':
    me = get_me()

    # ── LOGIN ──
    if not me:
        st.markdown(
            '<div class="banner"><div class="brand">🏦 Logit<span>rein</span> Bank</div>'
            '<div style="font-size:.82rem;color:#7a9bbf;margin-top:4px">Acesse sua conta com segurança</div></div>',
            unsafe_allow_html=True
        )
        _, col, _ = st.columns([1, 1.8, 1])
        with col:
            st.markdown(
                '<div style="background:#0f1929;border:1px solid rgba(0,201,167,.2);'
                'border-radius:14px;padding:28px"><div style="font-size:1.5rem;text-align:center">🏦</div>',
                unsafe_allow_html=True
            )
            login_input = st.text_input("Login", placeholder="Digite seu login", key="login_campo")
            senha_input = st.text_input("Senha", type="password", placeholder="••••••••", key="senha_campo")

            if st.button("🔑 Entrar no Sistema", use_container_width=True, type="primary"):
                users = get_users()
                user = next(
                    (u for u in users
                     if u['login'].lower() == login_input.lower().strip()
                     and u['senha'] == senha_input
                     and u['ativo']),
                    None
                )
                if user:
                    st.session_state.banco_user_id = user['id']
                    st.rerun()
                else:
                    st.error("❌ Login ou senha incorretos. Procure o gerente.")

            st.markdown(
                "<div style='font-size:.72rem;color:#3a5070;text-align:center;margin-top:10px'>"
                "Acesso restrito. Credenciais fornecidas pelo gerente da agência.</div>",
                unsafe_allow_html=True
            )

            # Dica de usuários para facilitar testes
            with st.expander("👤 Usuários de teste"):
                for u in get_users():
                    st.caption(f"**{u['login']}** / `{u['senha']}` — {ROLE_LABELS.get(u['role'], '')}")

        st.stop()

    # ── PAINEL DO USUÁRIO LOGADO ──
    role = me['role']
    cor_role = ROLE_CORES.get(role, '#00c9a7')

    # Menus por perfil
    menus_por_role = {
        'ceo':     ["📊 Dashboard","👥 Usuários","💰 Depósito","🏧 Saque","↔️ Transferência","⚡ Pix","📄 Boletos","📈 Investimentos","📋 Extrato"],
        'gerente': ["📊 Dashboard","👥 Usuários","💰 Depósito","🏧 Saque","↔️ Transferência","⚡ Pix","📄 Boletos","📈 Investimentos","📋 Extrato"],
        'pf':      ["📊 Dashboard","💰 Depósito","🏧 Saque","↔️ Transferência","⚡ Pix","📄 Boletos","📱 Recarga","💳 Cartões","🎁 Cashback","📈 Investimentos","💵 Crédito","📋 Extrato"],
        'pj':      ["📊 Dashboard","💰 Depósito","🏧 Saque","↔️ Transferência","⚡ Pix","📄 Boletos","💼 Folha","🔄 Fluxo","📈 Investimentos","🏦 Crédito PJ","📋 Extrato"],
        'salario': ["📊 Dashboard","🏧 Saque","↔️ Transferência","⚡ Pix","📱 Recarga","📋 Extrato"],
    }
    menus = menus_por_role.get(role, menus_por_role['pf'])

    # Header do usuário
    st.markdown(
        f'<div style="display:flex;align-items:center;justify-content:space-between;'
        f'padding:14px 0;margin-bottom:12px;border-bottom:1px solid rgba(255,255,255,.07)">'
        f'<div>'
        f'<div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;color:#fff">{me["nome"]}</div>'
        f'<div style="font-size:.72rem">'
        f'<span style="background:rgba(255,255,255,.07);padding:2px 9px;border-radius:99px;color:{cor_role}">'
        f'{ROLE_LABELS.get(role, "")}</span>'
        f'<span style="color:#5a7090;margin-left:8px">Ag {me["agencia"]} · Cta {me["conta"]}</span>'
        f'</div></div>'
        f'<div style="text-align:right">'
        f'<div style="font-size:.62rem;color:#5a7090">Saldo disponível</div>'
        f'<div style="font-family:Syne,sans-serif;font-size:1.4rem;font-weight:800;color:#22c55e">'
        f'{fmt(me["saldo"])}</div></div></div>',
        unsafe_allow_html=True
    )

    # Menu de navegação
    sel = st.radio("nav", menus, horizontal=True, label_visibility="collapsed", key="banco_nav")
    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)

    # ── DASHBOARD ──
    if "Dashboard" in sel:
        if role in ['ceo', 'gerente']:
            users = get_users()
            c1, c2, c3, c4 = st.columns(4)
            totais = [
                (c1, "Clientes Ativos", len([u for u in users if u['ativo']]), "#00c9a7"),
                (c2, "Saldo Total", fmt(sum(u.get('saldo', 0) for u in users)), "#22c55e"),
                (c3, "Crédito Concedido", fmt(sum(u.get('dividas', 0) for u in users)), "#e94b4b"),
                (c4, "Total Transações", sum(len(u.get('transacoes', [])) for u in users), "#f5c842"),
            ]
            for col, lbl, val, cor in totais:
                with col:
                    st.markdown(
                        f'<div class="metric-box"><div class="metric-label">{lbl}</div>'
                        f'<div class="metric-value" style="color:{cor}">{val}</div></div>',
                        unsafe_allow_html=True
                    )
            st.markdown("##### 👥 Todas as Contas")
            for u in users:
                cor2 = ROLE_CORES.get(u['role'], '#fff')
                status_icon = "✅" if u['ativo'] else "❌"
                st.markdown(
                    f'<div style="display:flex;justify-content:space-between;align-items:center;'
                    f'padding:8px 12px;background:rgba(255,255,255,.03);border-radius:8px;margin-bottom:4px;font-size:.82rem">'
                    f'<span>{status_icon} <strong style="color:#e2ecf8">{u["nome"]}</strong> '
                    f'<span style="color:{cor2};font-size:.65rem;margin-left:6px">{ROLE_LABELS.get(u["role"], "")}</span>'
                    f'<span style="color:#5a7090;font-size:.65rem;margin-left:6px">· {u["login"]}</span></span>'
                    f'<span style="color:#22c55e;font-weight:600">{fmt(u["saldo"])}</span></div>',
                    unsafe_allow_html=True
                )
        else:
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(
                    f'<div class="metric-box"><div class="metric-label">Conta Corrente</div>'
                    f'<div class="metric-value" style="color:#22c55e">{fmt(me["saldo"])}</div></div>',
                    unsafe_allow_html=True
                )
            with c2:
                st.markdown(
                    f'<div class="metric-box"><div class="metric-label">Poupança</div>'
                    f'<div class="metric-value" style="color:#00c9a7">{fmt(me.get("poupanca", 0))}</div></div>',
                    unsafe_allow_html=True
                )
            with c3:
                st.markdown(
                    f'<div class="metric-box"><div class="metric-label">Cashback</div>'
                    f'<div class="metric-value" style="color:#f5c842">{fmt(me.get("cashback", 0))}</div></div>',
                    unsafe_allow_html=True
                )
            txs = me.get('transacoes', [])[:6]
            if txs:
                st.markdown("##### Últimas transações")
                for tx in txs:
                    cor3 = "#22c55e" if tx['dir'] == 'in' else "#e94b4b"
                    sinal = "+" if tx['dir'] == 'in' else "-"
                    st.markdown(
                        f'<div class="tx-item">'
                        f'<div style="flex:1"><div style="color:#e2ecf8">{tx["desc"]}</div>'
                        f'<div style="color:#5a7090;font-size:.7rem">{tx["ts"]}</div></div>'
                        f'<div style="color:{cor3};font-weight:700;font-family:Syne,sans-serif">{sinal}{fmt(tx["valor"])}</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
            else:
                st.info("Nenhuma transação ainda. Use as opções acima para movimentar sua conta.")

    # ── DEPÓSITO ──
    elif "Depósito" in sel:
        st.markdown("#### 💰 Depósito")
        tipo = st.selectbox("Tipo", ["Dinheiro", "TED/DOC Recebido", "Cheque"])
        valor = st.number_input("Valor (R$)", min_value=0.01, step=10.0, key="dep_val")
        desc = st.text_input("Descrição (opcional)", placeholder="Ex: Salário", key="dep_desc")
        if st.button("✅ Confirmar Depósito", type="primary"):
            if valor <= 0:
                st.error("❌ Valor inválido.")
            else:
                update_saldo(me['id'], valor)
                add_tx(me['id'], 'deposito', f'Depósito — {desc or tipo}', valor, 'in')
                st.success(f"✅ Depósito de {fmt(valor)} realizado com sucesso!")
                st.rerun()

    # ── SAQUE ──
    elif "Saque" in sel:
        st.markdown("#### 🏧 Saque")
        st.markdown(
            f'<div class="metric-box" style="margin-bottom:16px">'
            f'<div class="metric-label">Saldo Disponível</div>'
            f'<div class="metric-value" style="color:#22c55e">{fmt(me["saldo"])}</div></div>',
            unsafe_allow_html=True
        )
        tipo = st.selectbox("Tipo", ["Caixa Eletrônico", "Caixa do Banco", "Lotérica"])
        valor = st.number_input("Valor (R$)", min_value=0.01, max_value=float(max(me['saldo'], 0.01)), step=10.0, key="saq_val")
        if st.button("✅ Confirmar Saque", type="primary"):
            if valor > me['saldo']:
                st.error("❌ Saldo insuficiente.")
            else:
                update_saldo(me['id'], -valor)
                add_tx(me['id'], 'saque', f'Saque — {tipo}', valor, 'out')
                st.success(f"✅ Saque de {fmt(valor)} realizado!")
                st.rerun()

    # ── TRANSFERÊNCIA ──
    elif "Transferência" in sel:
        st.markdown("#### ↔️ Transferência")
        banco_dest = st.selectbox("Banco destino", ["Logitrein Bank", "Banco do Brasil", "Bradesco", "Itaú", "Caixa", "Nubank", "Santander"])
        nome_dest = st.text_input("Nome do beneficiário", key="transf_nome")
        valor = st.number_input("Valor (R$)", min_value=0.01, step=10.0, key="transf_val")
        if st.button("✅ Transferir", type="primary"):
            if valor > me['saldo']:
                st.error("❌ Saldo insuficiente.")
            elif not nome_dest:
                st.error("❌ Informe o nome do beneficiário.")
            else:
                update_saldo(me['id'], -valor)
                add_tx(me['id'], 'transferencia', f'TED para {nome_dest} ({banco_dest})', valor, 'out')
                st.success(f"✅ Transferência de {fmt(valor)} para {nome_dest} realizada!")
                st.rerun()

    # ── PIX ──
    elif "Pix" in sel:
        st.markdown("#### ⚡ Pix")
        tipo_chave = st.selectbox("Tipo de chave", ["CPF", "CNPJ", "E-mail", "Telefone", "Chave Aleatória"])
        chave = st.text_input("Chave Pix", key="pix_chave")
        valor = st.number_input("Valor (R$)", min_value=0.01, step=10.0, key="pix_val")
        desc_pix = st.text_input("Descrição (opcional)", key="pix_desc")
        if st.button("⚡ Enviar Pix", type="primary"):
            if valor > me['saldo']:
                st.error("❌ Saldo insuficiente.")
            elif not chave:
                st.error("❌ Informe a chave Pix.")
            else:
                update_saldo(me['id'], -valor)
                add_tx(me['id'], 'pix', f'Pix → {chave} | {desc_pix or "Pix"}', valor, 'out')
                st.success(f"⚡ Pix de {fmt(valor)} enviado para {chave}!")
                st.rerun()

    # ── BOLETOS ──
    elif "Boletos" in sel:
        t1, t2 = st.tabs(["💳 Pagar Boleto", "📄 Emitir Boleto"])
        with t1:
            cod = st.text_input("Código de barras", key="bol_cod")
            valor = st.number_input("Valor (R$)", min_value=0.01, step=10.0, key="bol_val")
            if st.button("✅ Pagar Boleto", type="primary"):
                if valor > me['saldo']:
                    st.error("❌ Saldo insuficiente.")
                else:
                    update_saldo(me['id'], -valor)
                    add_tx(me['id'], 'boleto', f'Boleto — {cod[:20] if cod else "sem código"}', valor, 'out')
                    st.success(f"✅ Boleto de {fmt(valor)} pago!")
                    st.rerun()
        with t2:
            pagador = st.text_input("Nome do pagador", key="bol_pag")
            valor2 = st.number_input("Valor", min_value=0.01, step=10.0, key="bol_v2")
            desc2 = st.text_input("Descrição do boleto", key="bol_desc")
            venc = st.date_input("Vencimento", key="bol_venc")
            if st.button("📄 Gerar Boleto"):
                cod_g = ''.join(random.choices(string.digits, k=47))
                st.success(f"📄 Boleto gerado com sucesso!")
                st.code(f"Pagador: {pagador}\nValor: {fmt(valor2)}\nVencimento: {venc}\nDescrição: {desc2}\nCódigo: {cod_g}", language=None)

    # ── RECARGA ──
    elif "Recarga" in sel:
        st.markdown("#### 📱 Recarga de Celular")
        op = st.selectbox("Operadora", ["Claro", "Vivo", "TIM", "Oi", "CTBC"])
        num = st.text_input("Número do celular (DDD + número)", key="rec_num")
        valor = st.selectbox("Valor", [10, 20, 30, 50, 100], key="rec_val")
        if st.button("✅ Recarregar", type="primary"):
            if valor > me['saldo']:
                st.error("❌ Saldo insuficiente.")
            elif not num or len(num.replace(" ", "").replace("-", "")) < 10:
                st.error("❌ Número de celular inválido.")
            else:
                update_saldo(me['id'], -valor)
                add_tx(me['id'], 'recarga', f'Recarga {op} — {num}', valor, 'out')
                st.success(f"✅ Recarga de {fmt(valor)} para {num} ({op}) realizada!")
                st.rerun()

    # ── CARTÕES ──
    elif "Cartões" in sel:
        st.markdown("#### 💳 Cartões")
        cartoes = me.get('cartoes', [])
        if cartoes:
            cols_c = st.columns(min(len(cartoes), 3))
            for i, c in enumerate(cartoes):
                with cols_c[i % 3]:
                    bg = "linear-gradient(135deg,#1a56db,#0b1f3a)" if c["tipo"] == "Físico" else "linear-gradient(135deg,#0b3a3a,#0d2a55)"
                    st.markdown(
                        f'<div style="background:{bg};border-radius:14px;padding:20px;margin-bottom:12px">'
                        f'<div style="font-size:.6rem;color:rgba(255,255,255,.4);margin-bottom:14px">LOGITREIN BANK · {c["tipo"].upper()}</div>'
                        f'<div style="font-size:.9rem;letter-spacing:3px;color:rgba(255,255,255,.7);margin-bottom:14px">{c["num"]}</div>'
                        f'<div style="font-size:.75rem;color:#fff">{me["nome"][:20].upper()}</div></div>',
                        unsafe_allow_html=True
                    )
        else:
            st.info("Nenhum cartão emitido. Solicite abaixo.")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("+ Emitir Cartão Físico", use_container_width=True):
                users = get_users()
                for u in users:
                    if u['id'] == me['id']:
                        u.setdefault('cartoes', []).append({
                            "tipo": "Físico",
                            "num": f"**** **** **** {random.randint(1000, 9999)}"
                        })
                save_users(users)
                st.rerun()
        with col2:
            if st.button("+ Emitir Cartão Virtual", use_container_width=True):
                users = get_users()
                for u in users:
                    if u['id'] == me['id']:
                        u.setdefault('cartoes', []).append({
                            "tipo": "Virtual",
                            "num": f"**** **** **** {random.randint(1000, 9999)}"
                        })
                save_users(users)
                st.rerun()

    # ── CASHBACK ──
    elif "Cashback" in sel:
        st.markdown("#### 🎁 Cashback")
        cb = me.get('cashback', 0)
        st.markdown(
            f'<div class="metric-box"><div class="metric-label">Cashback Disponível</div>'
            f'<div class="metric-value" style="color:#f5c842">{fmt(cb)}</div></div>',
            unsafe_allow_html=True
        )
        st.markdown("##### 🛍️ Registrar Compra (ganha 5% de cashback)")
        desc_c = st.text_input("Descrição da compra", key="cb_desc")
        val_c = st.number_input("Valor da compra (R$)", min_value=0.01, step=10.0, key="cb_v")
        if st.button("🛍️ Registrar Compra"):
            if val_c > me['saldo']:
                st.error("❌ Saldo insuficiente.")
            else:
                cbv = val_c * 0.05
                update_saldo(me['id'], -val_c)
                add_tx(me['id'], 'compra', desc_c or 'Compra', val_c, 'out')
                users = get_users()
                for u in users:
                    if u['id'] == me['id']:
                        u['cashback'] = float(u.get('cashback', 0)) + cbv
                save_users(users)
                st.success(f"✅ Compra registrada! Cashback gerado: +{fmt(cbv)}")
                st.rerun()
        if cb > 0:
            if st.button("💰 Resgatar Cashback para Conta Corrente"):
                update_saldo(me['id'], cb)
                add_tx(me['id'], 'cashback', 'Resgate de Cashback', cb, 'in')
                users = get_users()
                for u in users:
                    if u['id'] == me['id']:
                        u['cashback'] = 0
                save_users(users)
                st.success(f"✅ {fmt(cb)} resgatado para sua conta!")
                st.rerun()

    # ── INVESTIMENTOS ──
    elif "Investimentos" in sel or "Investimento" in sel:
        st.markdown("#### 📈 Investimentos")
        opcoes = {
            "Poupança (0,5% a.m.)": "poupanca",
            "CDB 110% CDI": "investimentos",
            "Tesouro Direto": "investimentos",
            "LCI/LCA": "investimentos"
        }
        tipo_inv = st.selectbox("Produto", list(opcoes.keys()))
        val_inv = st.number_input("Valor (R$)", min_value=0.01, step=100.0, key="inv_val")
        if st.button("📈 Aplicar", type="primary"):
            if val_inv > me['saldo']:
                st.error("❌ Saldo insuficiente.")
            else:
                campo = opcoes[tipo_inv]
                update_saldo(me['id'], -val_inv)
                add_tx(me['id'], 'investimento', f'Aplicação — {tipo_inv}', val_inv, 'out')
                users = get_users()
                for u in users:
                    if u['id'] == me['id']:
                        u[campo] = float(u.get(campo, 0)) + val_inv
                save_users(users)
                st.success(f"✅ {fmt(val_inv)} aplicado em {tipo_inv}!")
                st.rerun()

        st.markdown("##### 📊 Suas Posições")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(
                f'<div class="metric-box"><div class="metric-label">Poupança</div>'
                f'<div class="metric-value" style="color:#00c9a7">{fmt(me.get("poupanca", 0))}</div></div>',
                unsafe_allow_html=True
            )
        with c2:
            st.markdown(
                f'<div class="metric-box"><div class="metric-label">CDB / Tesouro / LCI</div>'
                f'<div class="metric-value" style="color:#93b4f7">{fmt(me.get("investimentos", 0))}</div></div>',
                unsafe_allow_html=True
            )

    # ── CRÉDITO PF ──
    elif "Crédito" in sel and role == 'pf':
        st.markdown("#### 💵 Crédito Pessoal")
        tipo_cred = st.selectbox("Tipo", ["Empréstimo Pessoal", "Cheque Especial", "Consignado"])
        val_cred = st.number_input("Valor (R$)", min_value=100.0, step=100.0, key="cred_val")
        prazo = st.selectbox("Prazo (meses)", [6, 12, 18, 24, 36])
        taxa = 0.029
        if val_cred > 0:
            parc = val_cred * taxa / (1 - (1 + taxa) ** (-prazo))
            st.info(f"💡 Parcela estimada: {fmt(parc)}/mês | Total: {fmt(parc * prazo)} | Taxa: 2,9% a.m.")
        if st.button("✅ Solicitar Crédito", type="primary"):
            update_saldo(me['id'], val_cred)
            add_tx(me['id'], 'credito', f'{tipo_cred} aprovado', val_cred, 'in')
            users = get_users()
            for u in users:
                if u['id'] == me['id']:
                    u['dividas'] = float(u.get('dividas', 0)) + val_cred
            save_users(users)
            st.success(f"✅ {fmt(val_cred)} aprovado e creditado na sua conta!")
            st.rerun()

    # ── CRÉDITO PJ ──
    elif "Crédito PJ" in sel and role == 'pj':
        st.markdown("#### 🏦 Crédito Empresarial")
        tipo_cred = st.selectbox("Tipo", ["Capital de Giro", "Financiamento de Equipamentos", "Antecipação de Recebíveis"])
        val_cred = st.number_input("Valor (R$)", min_value=100.0, step=500.0, key="credpj_val")
        prazo = st.selectbox("Prazo (meses)", [6, 12, 18, 24, 36])
        taxa = 0.012
        if val_cred > 0:
            parc = val_cred * taxa / (1 - (1 + taxa) ** (-prazo))
            st.info(f"💡 Parcela: {fmt(parc)}/mês | Total: {fmt(parc * prazo)} | Taxa: 1,2% a.m. PJ")
        if st.button("✅ Solicitar Crédito PJ", type="primary"):
            update_saldo(me['id'], val_cred)
            add_tx(me['id'], 'credito', f'{tipo_cred} aprovado', val_cred, 'in')
            users = get_users()
            for u in users:
                if u['id'] == me['id']:
                    u['dividas'] = float(u.get('dividas', 0)) + val_cred
            save_users(users)
            st.success(f"✅ {fmt(val_cred)} aprovado!")
            st.rerun()

    # ── FOLHA DE PAGAMENTO PJ ──
    elif "Folha" in sel:
        st.markdown("#### 💼 Folha de Pagamento")
        n_func = st.number_input("Nº de funcionários", min_value=1, step=1, key="folha_n")
        sal_med = st.number_input("Salário médio (R$)", min_value=0.01, step=100.0, key="folha_s")
        if n_func > 0 and sal_med > 0:
            total = n_func * sal_med
            enc = total * 0.28
            grand = total + enc
            st.info(f"📋 Salários: {fmt(total)} | Encargos (28%): {fmt(enc)} | **Total: {fmt(grand)}**")
        if st.button("💼 Processar Folha", type="primary"):
            grand = n_func * sal_med * 1.28
            if grand > me['saldo']:
                st.error(f"❌ Saldo insuficiente. Necessário: {fmt(grand)} | Disponível: {fmt(me['saldo'])}")
            else:
                update_saldo(me['id'], -grand)
                add_tx(me['id'], 'folha', f'Folha de pagamento — {int(n_func)} funcionários', grand, 'out')
                st.success(f"✅ Folha processada! Total debitado: {fmt(grand)}")
                st.rerun()

    # ── FLUXO DE CAIXA ──
    elif "Fluxo" in sel:
        st.markdown("#### 🔄 Fluxo de Caixa")
        txs = me.get('transacoes', [])
        ent = sum(t['valor'] for t in txs if t['dir'] == 'in')
        sai = sum(t['valor'] for t in txs if t['dir'] == 'out')
        liq = ent - sai
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(
                f'<div class="metric-box"><div class="metric-label">Total Entradas</div>'
                f'<div class="metric-value" style="color:#22c55e">{fmt(ent)}</div></div>',
                unsafe_allow_html=True
            )
        with c2:
            st.markdown(
                f'<div class="metric-box"><div class="metric-label">Total Saídas</div>'
                f'<div class="metric-value" style="color:#e94b4b">{fmt(sai)}</div></div>',
                unsafe_allow_html=True
            )
        with c3:
            cor_liq = "#22c55e" if liq >= 0 else "#e94b4b"
            st.markdown(
                f'<div class="metric-box"><div class="metric-label">Líquido</div>'
                f'<div class="metric-value" style="color:{cor_liq}">{fmt(liq)}</div></div>',
                unsafe_allow_html=True
            )
        st.markdown("##### Histórico de Movimentações")
        if not txs:
            st.info("Nenhuma transação registrada.")
        for tx in txs:
            cor3 = "#22c55e" if tx['dir'] == 'in' else "#e94b4b"
            sinal = "+" if tx['dir'] == 'in' else "-"
            st.markdown(
                f'<div class="tx-item">'
                f'<div style="flex:1"><div style="color:#e2ecf8">{tx["desc"]}</div>'
                f'<div style="color:#5a7090;font-size:.7rem">{tx["ts"]}</div></div>'
                f'<div style="color:{cor3};font-weight:700">{sinal}{fmt(tx["valor"])}</div></div>',
                unsafe_allow_html=True
            )

    # ── EXTRATO ──
    elif "Extrato" in sel:
        st.markdown("#### 📋 Extrato Completo")
        txs = me.get('transacoes', [])
        if not txs:
            st.info("Nenhuma transação ainda.")
        else:
            st.caption(f"{len(txs)} transações registradas")
            for tx in txs:
                cor3 = "#22c55e" if tx['dir'] == 'in' else "#e94b4b"
                sinal = "+" if tx['dir'] == 'in' else "-"
                tipo_badge = {
                    'deposito': '#22c55e', 'saque': '#e94b4b', 'transferencia': '#93b4f7',
                    'pix': '#f59e0b', 'boleto': '#a78bfa', 'credito': '#34d399',
                    'investimento': '#60a5fa', 'cashback': '#f5c842', 'recarga': '#fb923c',
                    'folha': '#f87171', 'compra': '#e94b4b'
                }.get(tx.get('tipo', ''), '#888')
                st.markdown(
                    f'<div class="tx-item">'
                    f'<span class="badge" style="background:{tipo_badge}22;color:{tipo_badge}">'
                    f'{tx.get("tipo", "—")}</span>'
                    f'<div style="flex:1"><div style="color:#e2ecf8">{tx["desc"]}</div>'
                    f'<div style="color:#5a7090;font-size:.7rem">{tx["ts"]}</div></div>'
                    f'<div style="color:{cor3};font-weight:700">{sinal}{fmt(tx["valor"])}</div></div>',
                    unsafe_allow_html=True
                )

    # ── GERENCIAR USUÁRIOS (Gerente / CEO) ──
    elif "Usuários" in sel:
        st.markdown("#### 👥 Gerenciar Usuários")
        users = get_users()
        # Gerente não pode editar CEO ou outros gerentes
        can_edit = [u for u in users if not (me['role'] == 'gerente' and u['role'] in ['ceo', 'gerente'])]

        with st.expander("➕ Criar Novo Usuário"):
            c1, c2, c3 = st.columns(3)
            with c1:
                nu_nome = st.text_input("Nome completo", key="nu_n")
            with c2:
                nu_login = st.text_input("Login", key="nu_l")
            with c3:
                nu_senha = st.text_input("Senha", type="password", key="nu_s")
            c4, c5 = st.columns(2)
            with c4:
                roles_disp = ["pf", "pj", "salario"] if me['role'] == 'gerente' else ["pf", "pj", "salario", "gerente"]
                nu_role_label = st.selectbox("Perfil", [ROLE_LABELS[r] for r in roles_disp], key="nu_r")
                nu_role_val = roles_disp[[ROLE_LABELS[r] for r in roles_disp].index(nu_role_label)]
            with c5:
                nu_saldo = st.number_input("Saldo inicial (R$)", min_value=0.0, step=100.0, key="nu_sl")

            if st.button("✅ Criar Usuário", type="primary"):
                if not nu_nome or not nu_login or not nu_senha:
                    st.error("❌ Preencha todos os campos obrigatórios.")
                elif any(u['login'].lower() == nu_login.lower() for u in users):
                    st.error("❌ Este login já existe. Escolha outro.")
                elif len(nu_senha) < 4:
                    st.error("❌ Senha deve ter no mínimo 4 caracteres.")
                else:
                    novo_id = f"u{len(users)+1}{random.randint(100, 999)}"
                    novo_conta = f"{10000 + len(users)}-{random.randint(0, 9)}"
                    novo = {
                        "id": novo_id, "login": nu_login, "senha": nu_senha,
                        "nome": nu_nome, "role": nu_role_val,
                        "agencia": "0001", "conta": novo_conta,
                        "saldo": float(nu_saldo), "poupanca": 0, "investimentos": 0,
                        "cashback": 0, "dividas": 0, "cartoes": [], "transacoes": [], "ativo": True
                    }
                    users.append(novo)
                    save_users(users)
                    st.success(f"✅ Usuário '{nu_nome}' criado! Login: **{nu_login}**")
                    st.rerun()

        st.markdown("---")
        for u in can_edit:
            cor2 = ROLE_CORES.get(u['role'], '#fff')
            c1, c2, c3, c4 = st.columns([3, 2, 1, 1])
            with c1:
                status_txt = "✅ Ativo" if u['ativo'] else "❌ Bloqueado"
                st.markdown(
                    f"**{u['nome']}** "
                    f"<span style='color:{cor2};font-size:.7rem'>{ROLE_LABELS.get(u['role'], '')}</span> "
                    f"<span style='color:#5a7090;font-size:.7rem'>· {u['login']} · {status_txt}</span>",
                    unsafe_allow_html=True
                )
            with c2:
                st.markdown(f"<span style='color:#22c55e;font-weight:600'>{fmt(u['saldo'])}</span>", unsafe_allow_html=True)
            with c3:
                btn_label = "🔓" if not u['ativo'] else "🔒"
                btn_help = "Desbloquear" if not u['ativo'] else "Bloquear"
                if st.button(btn_label, key=f"tog_{u['id']}", help=btn_help):
                    for usr in users:
                        if usr['id'] == u['id']:
                            usr['ativo'] = not usr['ativo']
                    save_users(users)
                    st.rerun()
            with c4:
                if st.button("💰", key=f"adj_{u['id']}", help="Ajustar saldo"):
                    st.session_state['adj_uid'] = u['id']

        # Ajuste de saldo inline
        if st.session_state.get('adj_uid'):
            uid_adj = st.session_state.adj_uid
            u_nome_adj = next((u['nome'] for u in users if u['id'] == uid_adj), '?')
            st.markdown(f"---\n**💰 Ajustar saldo de: {u_nome_adj}**")
            adj_val = st.number_input(
                "Valor (positivo = crédito, negativo = débito)",
                step=100.0, key="adj_v"
            )
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("✅ Confirmar Ajuste", type="primary"):
                    update_saldo(uid_adj, adj_val)
                    direcao = 'in' if adj_val >= 0 else 'out'
                    add_tx(uid_adj, 'deposito', f'Ajuste manual por {me["nome"]}', abs(adj_val), direcao)
                    del st.session_state['adj_uid']
                    st.success(f"✅ Saldo de {u_nome_adj} ajustado em {fmt(adj_val)}!")
                    st.rerun()
            with col_b:
                if st.button("❌ Cancelar"):
                    del st.session_state['adj_uid']
                    st.rerun()

# ══════════════════════════════════════════════
#  TELA: ADMIN
# ══════════════════════════════════════════════
elif tela == 'admin':
    if not st.session_state.admin_ok:
        st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
        _, col, _ = st.columns([1, 1.4, 1])
        with col:
            st.markdown(
                '<div style="background:#0f1929;border:1px solid rgba(245,200,66,.2);'
                'border-radius:14px;padding:28px;text-align:center">'
                '<div style="font-size:2rem">🔐</div>'
                '<div style="font-family:Syne,sans-serif;color:#f5c842;font-weight:700;margin:8px 0">Área Restrita</div>'
                '<div style="font-size:.73rem;color:#3a5070">Acesso exclusivo ao proprietário.</div></div>',
                unsafe_allow_html=True
            )
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            senha_adm = st.text_input(
                "", type="password", placeholder="Senha de administrador",
                label_visibility="collapsed", key="adm_senha"
            )
            if st.button("🔓 Entrar", use_container_width=True, type="primary"):
                if checar_admin(senha_adm):
                    st.session_state.admin_ok = True
                    st.rerun()
                else:
                    st.error("❌ Acesso negado. Senha incorreta.")
    else:
        st.markdown(
            '<div style="padding:12px 16px;background:#0f1929;border:1px solid rgba(245,200,66,.2);'
            'border-radius:10px;margin-bottom:18px">'
            '<span style="font-family:Syne,sans-serif;font-size:1rem;font-weight:800;color:#f5c842">⚙️ Painel Administrativo</span> '
            '<span style="font-size:.7rem;color:#5a7090">Jorge Zensque — Proprietário</span></div>',
            unsafe_allow_html=True
        )

        tab1, tab2, tab3 = st.tabs(["📁 Arquivos HTML", "👥 Banco — Visão Geral", "🔑 Segurança"])

        with tab1:
            st.caption("Upload de versões novas sem acessar o GitHub.")
            c1, c2 = st.columns(2)
            with c1:
                f_lt = lt_file() or 'logitrein.html'
                status_lt = f'✅ {get_size(f_lt)}' if file_exists(f_lt) else '❌ Não encontrado'
                st.markdown(f"**🏭 Logitrein** `{f_lt}` — {status_lt}")
                up = st.file_uploader("Enviar novo Logitrein (.html)", type=['html'], key='up_lt')
                if up:
                    dest = Path(__file__).parent / 'logitrein.html'
                    dest.write_bytes(up.read())
                    st.success("✅ Logitrein atualizado!")
                    st.rerun()
            with c2:
                st.markdown("**🏦 Banco** — Integrado em Python")
                st.info("O banco está integrado neste portal via session_state. Não depende de arquivo HTML.")

        with tab2:
            st.markdown("##### 👥 Usuários do Banco")
            users_adm = get_users()
            for u in users_adm:
                cor2 = ROLE_CORES.get(u['role'], '#fff')
                st.markdown(
                    f'<div style="display:flex;justify-content:space-between;padding:8px 12px;'
                    f'background:rgba(255,255,255,.03);border-radius:8px;margin-bottom:4px;font-size:.82rem">'
                    f'<span><strong style="color:#e2ecf8">{u["nome"]}</strong> '
                    f'<span style="color:{cor2};font-size:.65rem;margin-left:6px">{ROLE_LABELS.get(u["role"], "")}</span>'
                    f'<span style="color:#5a7090;font-size:.65rem;margin-left:6px">· login: {u["login"]}</span></span>'
                    f'<span style="color:#22c55e;font-weight:600">{fmt(u["saldo"])}</span></div>',
                    unsafe_allow_html=True
                )
            total_geral = sum(u.get('saldo', 0) for u in users_adm)
            st.markdown(f"**Total em caixa: {fmt(total_geral)}**")

        with tab3:
            st.markdown("##### 🔑 Alterar Senha Admin")
            n1 = st.text_input("Nova senha admin", type="password", placeholder="Mínimo 8 caracteres", key="adm_n1")
            n2 = st.text_input("Confirmar senha", type="password", key="adm_n2")
            if st.button("🔑 Gerar hash da nova senha"):
                if len(n1) < 8:
                    st.error("❌ Mínimo 8 caracteres.")
                elif n1 != n2:
                    st.error("❌ Senhas não conferem.")
                else:
                    h = hashlib.sha256(n1.encode()).hexdigest()
                    st.success("✅ Cole este hash no app.py na variável ADMIN_HASH:")
                    st.code(f'ADMIN_HASH = "{h}"', language="python")

            st.markdown("---")
            if st.button("🚪 Sair do Admin"):
                st.session_state.admin_ok = False
                st.session_state.tela = 'portal'
                st.rerun()
