"""
Logitrein Portal v7.0 — Banco 100% em Python/Streamlit (sem localStorage)
"""
import streamlit as st
import hashlib
import json
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

# ══════════════════════════════════════════════
#  BANCO — dados em st.session_state (funciona 100% no Streamlit)
# ══════════════════════════════════════════════
USUARIOS_PADRAO = [
    {"id":"u0","login":"ceo",         "senha":"ceo123",   "nome":"Roberto Logitrein","role":"ceo",     "agencia":"0001","conta":"00001-0","saldo":50000.0,"poupanca":0,"investimentos":0,"cashback":0,"dividas":0,"cartoes":[],"transacoes":[],"ativo":True},
    {"id":"u1","login":"gerente1",     "senha":"ger123",   "nome":"Ana Gerente",      "role":"gerente", "agencia":"0001","conta":"00002-1","saldo":15000.0,"poupanca":0,"investimentos":0,"cashback":0,"dividas":0,"cartoes":[],"transacoes":[],"ativo":True},
    {"id":"u2","login":"joao.silva",   "senha":"123456",   "nome":"João da Silva",    "role":"pf",      "agencia":"0001","conta":"10001-2","saldo":3500.0, "poupanca":500,"investimentos":0,"cashback":0,"dividas":0,"cartoes":[],"transacoes":[],"ativo":True},
    {"id":"u3","login":"emp.ltda",     "senha":"empresa1", "nome":"Empresa Logitrein","role":"pj",      "agencia":"0001","conta":"20001-3","saldo":25000.0,"poupanca":0,"investimentos":0,"cashback":0,"dividas":0,"cartoes":[],"transacoes":[],"ativo":True},
    {"id":"u4","login":"maria.santos", "senha":"salario1", "nome":"Maria dos Santos", "role":"salario", "agencia":"0001","conta":"30001-4","saldo":2800.0, "poupanca":0,"investimentos":0,"cashback":0,"dividas":0,"cartoes":[],"transacoes":[],"empregador":"Empresa Logitrein","ativo":True},
]

ROLE_LABELS = {"ceo":"CEO","gerente":"Gerente","pf":"Pessoa Física","pj":"Pessoa Jurídica","salario":"Conta Salário"}
ROLE_CORES  = {"ceo":"#f5c842","gerente":"#93b4f7","pf":"#00c9a7","pj":"#fdba74","salario":"#86efac"}

def init_banco():
    if 'banco_users' not in st.session_state:
        st.session_state.banco_users = json.loads(json.dumps(USUARIOS_PADRAO))
    if 'banco_user_id' not in st.session_state:
        st.session_state.banco_user_id = None

def get_users():  return st.session_state.banco_users
def save_users(u): st.session_state.banco_users = u
def get_me():
    uid = st.session_state.banco_user_id
    return next((u for u in get_users() if u['id']==uid), None)

def fmt(v): return f"R$ {float(v or 0):,.2f}".replace(",","X").replace(".",",").replace("X",".")
def ts(): return datetime.now().strftime("%d/%m/%Y %H:%M")

def add_tx(uid, tipo, desc, valor, direcao):
    users = get_users()
    for u in users:
        if u['id']==uid:
            u.setdefault('transacoes',[]).insert(0,{"tipo":tipo,"desc":desc,"valor":float(valor),"dir":direcao,"ts":ts()})
    save_users(users)

def update_saldo(uid, delta):
    users = get_users()
    for u in users:
        if u['id']==uid: u['saldo'] = float(u.get('saldo',0)) + delta
    save_users(users)

# ══════════════════════════════════════════════
#  CSS GLOBAL
# ══════════════════════════════════════════════
st.set_page_config(page_title="Logitrein — Portal", page_icon="🏦", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif!important;background:#09182e!important;color:#ddeaf8!important}
.main,section[data-testid="stMain"]{background:#09182e!important}
.block-container{padding:1.5rem 2rem!important;max-width:1100px}
.banner{background:linear-gradient(135deg,#112240,#0d2a55);border:1px solid rgba(0,201,167,.15);border-radius:16px;padding:24px 28px;margin-bottom:18px}
.brand{font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;color:#00c9a7}
.brand span{color:#f5c842}
.card{background:#132240;border:1px solid rgba(255,255,255,.07);border-radius:12px;padding:18px}
.metric-box{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.07);border-radius:10px;padding:14px;text-align:center;margin-bottom:10px}
.metric-label{font-size:.6rem;color:#7a9bbf;text-transform:uppercase;letter-spacing:.8px}
.metric-value{font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:700}
.tx-item{display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid rgba(255,255,255,.05);font-size:.82rem}
.tx-item:last-child{border:none}
.badge{display:inline-block;padding:2px 8px;border-radius:99px;font-size:.58rem;font-weight:700;text-transform:uppercase;letter-spacing:.6px}
#MainMenu,footer,header,.stDeployButton{visibility:hidden!important;display:none!important}
section[data-testid="stSidebar"]{background:#112240!important}
.stTextInput input,.stNumberInput input,.stSelectbox select{background:rgba(255,255,255,.05)!important;border:1px solid rgba(255,255,255,.1)!important;color:#e2ecf8!important;border-radius:8px!important}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  ESTADO
# ══════════════════════════════════════════════
init_banco()
for k,v in [('tela','portal'),('banco_tela','login'),('admin_ok',False)]:
    if k not in st.session_state: st.session_state[k]=v

# ══════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════
with st.sidebar:
    st.markdown("<div style='font-family:Syne,sans-serif;font-size:.9rem;font-weight:800;color:#00c9a7;padding:4px 0 10px;border-bottom:1px solid rgba(255,255,255,.07);margin-bottom:8px'>🏦 Logitrein Portal</div>", unsafe_allow_html=True)
    if st.button("🏠 Portal", use_container_width=True):
        st.session_state.tela='portal'; st.rerun()
    if st.button("🏭 Logitrein v12", use_container_width=True, disabled=lt_file() is None):
        st.session_state.tela='logitrein'; st.rerun()
    if st.button("🏦 Banco Logitrein", use_container_width=True):
        st.session_state.tela='banco'; st.rerun()
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    if st.button("⚙️ Admin", use_container_width=False):
        st.session_state.tela='admin'; st.rerun()
    # Logout banco
    if st.session_state.banco_user_id:
        me = get_me()
        if me:
            st.markdown(f"<div style='margin-top:16px;padding:8px;background:rgba(0,201,167,.07);border-radius:8px;font-size:.75rem'><div style='color:#00c9a7;font-weight:600'>{me['nome'][:20]}</div><div style='color:#5a7090'>{ROLE_LABELS.get(me['role'],'')} · {fmt(me['saldo'])}</div></div>", unsafe_allow_html=True)
            if st.button("🚪 Sair do Banco", use_container_width=True):
                st.session_state.banco_user_id = None
                st.session_state.banco_tela = 'login'
                st.rerun()
    st.markdown(f"<div style='font-size:.58rem;color:#1e2d45;margin-top:12px'>v7.0 · {datetime.now().strftime('%d/%m/%Y')}</div>", unsafe_allow_html=True)

tela = st.session_state.tela

# ══════════════════════════════════════════════
#  PORTAL
# ══════════════════════════════════════════════
if tela == 'portal':
    st.markdown('<div class="banner"><div class="brand">🏭 Logit<span>rein</span> · 🏦 Banco</div><div style="font-size:.85rem;color:#7a9bbf;margin-top:4px">Portal integrado · Palmas/TO</div></div>', unsafe_allow_html=True)
    c1,c2 = st.columns(2,gap="large")
    with c1:
        st.markdown('<div class="card"><div style="font-family:Syne,sans-serif;font-weight:700;font-size:1rem;color:#fff;margin-bottom:6px">🏭 Logitrein v12</div><div style="font-size:.81rem;color:#7a9bbf;line-height:1.5">Gestão operacional, equipes, ponto e DP integrado.</div><div style="font-size:.7rem;color:#2a4060;margin-top:8px">Acesse com credenciais do coordenador.</div></div>', unsafe_allow_html=True)
        if st.button("🚀 Abrir Logitrein v12", use_container_width=True, disabled=lt_file() is None):
            st.session_state.tela='logitrein'; st.rerun()
    with c2:
        st.markdown('<div class="card"><div style="font-family:Syne,sans-serif;font-weight:700;font-size:1rem;color:#fff;margin-bottom:6px">🏦 Banco Logitrein</div><div style="font-size:.81rem;color:#7a9bbf;line-height:1.5">Conta corrente, Pix, transferências, crédito e investimentos.</div><div style="font-size:.7rem;color:#2a4060;margin-top:8px">Acesse com credenciais do gerente.</div></div>', unsafe_allow_html=True)
        if st.button("🏦 Abrir Banco Logitrein", use_container_width=True):
            st.session_state.tela='banco'; st.rerun()
    st.markdown('<div style="background:rgba(0,201,167,.07);border:1px solid rgba(0,201,167,.18);border-radius:10px;padding:12px 16px;font-size:.79rem;color:#6ee7da;margin-top:14px;line-height:1.6">🔗 <strong>Integração automática:</strong> Ao fechar a folha no Logitrein, os salários são depositados nas contas do Banco.</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  LOGITREIN
# ══════════════════════════════════════════════
elif tela == 'logitrein':
    f = lt_file()
    if f:
        p = Path(__file__).parent / f
        st.components.v1.html(p.read_text(encoding='utf-8'), height=950, scrolling=True)
    else:
        st.error("Arquivo não encontrado.")

# ══════════════════════════════════════════════
#  BANCO — 100% Python, sem localStorage
# ══════════════════════════════════════════════
elif tela == 'banco':
    me = get_me()

    # ── LOGIN ──
    if not me:
        st.markdown('<div class="banner"><div class="brand">🏦 Logit<span>rein</span> Bank</div><div style="font-size:.82rem;color:#7a9bbf;margin-top:4px">Acesse sua conta com segurança</div></div>', unsafe_allow_html=True)
        _,col,_ = st.columns([1,1.8,1])
        with col:
            login_input = st.text_input("Login", placeholder="Digite seu login")
            senha_input = st.text_input("Senha", type="password", placeholder="••••••••")
            if st.button("🔑 Entrar no Sistema", use_container_width=True, type="primary"):
                users = get_users()
                user = next((u for u in users if u['login'].lower()==login_input.lower().strip() and u['senha']==senha_input and u['ativo']), None)
                if user:
                    st.session_state.banco_user_id = user['id']
                    st.rerun()
                else:
                    st.error("❌ Login ou senha incorretos. Procure o gerente.")
            st.markdown("<div style='font-size:.72rem;color:#3a5070;text-align:center;margin-top:10px'>Acesso restrito. Credenciais fornecidas pelo gerente da agência.</div>", unsafe_allow_html=True)
        st.stop()

    # ── PAINEL DO USUÁRIO ──
    role = me['role']

    # Menu horizontal por role
    if role in ['ceo','gerente']:
        menus = ["📊 Dashboard","👥 Usuários","💰 Depósito","🏧 Saque","↔️ Transferência","⚡ Pix","📄 Boletos","📈 Investimentos","📋 Extrato"]
    elif role == 'pf':
        menus = ["📊 Dashboard","💰 Depósito","🏧 Saque","↔️ Transferência","⚡ Pix","📄 Boletos","📱 Recarga","💳 Cartões","🎁 Cashback","📈 Investimentos","💵 Crédito","📋 Extrato"]
    elif role == 'pj':
        menus = ["📊 Dashboard","💰 Depósito","🏧 Saque","↔️ Transferência","⚡ Pix","📄 Boletos","💼 Folha","🔄 Fluxo","📈 Investimentos","🏦 Crédito PJ","📋 Extrato"]
    else:  # salario
        menus = ["📊 Dashboard","🏧 Saque","↔️ Transferência","⚡ Pix","📱 Recarga","📋 Extrato"]

    if 'banco_menu' not in st.session_state: st.session_state.banco_menu = menus[0]

    # Header
    cor = ROLE_CORES.get(role,'#00c9a7')
    st.markdown(f'<div style="display:flex;align-items:center;justify-content:space-between;padding:14px 0;margin-bottom:12px;border-bottom:1px solid rgba(255,255,255,.07)"><div><div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;color:#fff">{me["nome"]}</div><div style="font-size:.72rem"><span style="background:rgba(255,255,255,.07);padding:2px 9px;border-radius:99px;color:{cor}">{ROLE_LABELS.get(role,"")}</span> <span style="color:#5a7090;margin-left:8px">Ag {me["agencia"]} · Cta {me["conta"]}</span></div></div><div style="text-align:right"><div style="font-size:.62rem;color:#5a7090">Saldo disponível</div><div style="font-family:Syne,sans-serif;font-size:1.4rem;font-weight:800;color:#22c55e">{fmt(me["saldo"])}</div></div></div>', unsafe_allow_html=True)

    # Menu tabs
    sel = st.radio("", menus, horizontal=True, label_visibility="collapsed", key="banco_nav")

    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)

    # ── DASHBOARD ──
    if "Dashboard" in sel:
        if role in ['ceo','gerente']:
            users = get_users()
            c1,c2,c3,c4 = st.columns(4)
            totais = [(c1,"Clientes",len([u for u in users if u['ativo']]),"#00c9a7"),
                      (c2,"Saldo Total",fmt(sum(u.get('saldo',0) for u in users)),"#22c55e"),
                      (c3,"Crédito",fmt(sum(u.get('dividas',0) for u in users)),"#e94b4b"),
                      (c4,"Transações",sum(len(u.get('transacoes',[])) for u in users),"#f5c842")]
            for col,lbl,val,cor in totais:
                with col: st.markdown(f'<div class="metric-box"><div class="metric-label">{lbl}</div><div class="metric-value" style="color:{cor}">{val}</div></div>',unsafe_allow_html=True)
            st.markdown("##### 👥 Contas")
            for u in users:
                cor2 = ROLE_CORES.get(u['role'],'#fff')
                st.markdown(f'<div style="display:flex;justify-content:space-between;padding:8px 12px;background:rgba(255,255,255,.03);border-radius:8px;margin-bottom:4px;font-size:.82rem"><span><strong style="color:#e2ecf8">{u["nome"]}</strong> <span style="color:{cor2};font-size:.65rem;margin-left:6px">{ROLE_LABELS.get(u["role"],"")}</span></span><span style="color:#22c55e;font-weight:600">{fmt(u["saldo"])}</span></div>',unsafe_allow_html=True)
        else:
            c1,c2,c3 = st.columns(3)
            with c1: st.markdown(f'<div class="metric-box"><div class="metric-label">Conta Corrente</div><div class="metric-value" style="color:#22c55e">{fmt(me["saldo"])}</div></div>',unsafe_allow_html=True)
            with c2: st.markdown(f'<div class="metric-box"><div class="metric-label">Poupança</div><div class="metric-value" style="color:#00c9a7">{fmt(me.get("poupanca",0))}</div></div>',unsafe_allow_html=True)
            with c3: st.markdown(f'<div class="metric-box"><div class="metric-label">Cashback</div><div class="metric-value" style="color:#f5c842">{fmt(me.get("cashback",0))}</div></div>',unsafe_allow_html=True)
            txs = me.get('transacoes',[])[:6]
            if txs:
                st.markdown("##### Últimas transações")
                for tx in txs:
                    cor3 = "#22c55e" if tx['dir']=='in' else "#e94b4b"
                    sinal = "+" if tx['dir']=='in' else "-"
                    st.markdown(f'<div class="tx-item"><div style="flex:1"><div style="color:#e2ecf8">{tx["desc"]}</div><div style="color:#5a7090;font-size:.7rem">{tx["ts"]}</div></div><div style="color:{cor3};font-weight:700;font-family:Syne,sans-serif">{sinal}{fmt(tx["valor"])}</div></div>',unsafe_allow_html=True)

    # ── DEPÓSITO ──
    elif "Depósito" in sel:
        st.markdown("#### 💰 Depósito")
        tipo = st.selectbox("Tipo",["Dinheiro","TED/DOC Recebido","Cheque"])
        valor = st.number_input("Valor (R$)", min_value=0.01, step=10.0)
        desc = st.text_input("Descrição (opcional)", placeholder="Ex: Salário")
        if st.button("✅ Confirmar Depósito", type="primary"):
            update_saldo(me['id'], valor)
            add_tx(me['id'],'deposito',f'Depósito — {desc or tipo}',valor,'in')
            st.success(f"✅ Depósito de {fmt(valor)} realizado!"); st.rerun()

    # ── SAQUE ──
    elif "Saque" in sel:
        st.markdown("#### 🏧 Saque")
        if role=='salario':
            st.markdown(f'<div class="metric-box" style="margin-bottom:16px"><div class="metric-label">Saldo Disponível</div><div class="metric-value" style="color:#22c55e">{fmt(me["saldo"])}</div></div>',unsafe_allow_html=True)
        tipo = st.selectbox("Tipo",["Caixa Eletrônico","Caixa do Banco","Lotérica"])
        valor = st.number_input("Valor (R$)", min_value=0.01, step=10.0)
        if st.button("✅ Confirmar Saque", type="primary"):
            if valor > me['saldo']: st.error("❌ Saldo insuficiente.")
            else:
                update_saldo(me['id'], -valor)
                add_tx(me['id'],'saque',f'Saque — {tipo}',valor,'out')
                st.success(f"✅ Saque de {fmt(valor)} realizado!"); st.rerun()

    # ── TRANSFERÊNCIA ──
    elif "Transferência" in sel:
        st.markdown("#### ↔️ Transferência")
        banco_dest = st.selectbox("Banco",["Logitrein Bank","Banco do Brasil","Bradesco","Itaú","Caixa","Nubank","Santander"])
        nome_dest = st.text_input("Nome do beneficiário")
        valor = st.number_input("Valor (R$)", min_value=0.01, step=10.0)
        if st.button("✅ Transferir", type="primary"):
            if valor > me['saldo']: st.error("❌ Saldo insuficiente.")
            else:
                update_saldo(me['id'], -valor)
                add_tx(me['id'],'transferencia',f'TED para {nome_dest or "Beneficiário"}',valor,'out')
                st.success(f"✅ Transferência de {fmt(valor)} para {nome_dest} realizada!"); st.rerun()

    # ── PIX ──
    elif "Pix" in sel:
        st.markdown("#### ⚡ Pix")
        tipo_chave = st.selectbox("Tipo de chave",["CPF","CNPJ","E-mail","Telefone","Chave Aleatória"])
        chave = st.text_input("Chave Pix")
        valor = st.number_input("Valor (R$)", min_value=0.01, step=10.0)
        desc = st.text_input("Descrição (opcional)")
        if st.button("⚡ Enviar Pix", type="primary"):
            if valor > me['saldo']: st.error("❌ Saldo insuficiente.")
            else:
                update_saldo(me['id'], -valor)
                add_tx(me['id'],'pix',f'Pix → {chave or "—"} | {desc or "Pix"}',valor,'out')
                st.success(f"⚡ Pix de {fmt(valor)} enviado!"); st.rerun()

    # ── BOLETOS ──
    elif "Boletos" in sel:
        t1,t2 = st.tabs(["Pagar Boleto","Emitir Boleto"])
        with t1:
            cod = st.text_input("Código de barras")
            valor = st.number_input("Valor (R$)", min_value=0.01, step=10.0)
            if st.button("✅ Pagar", type="primary"):
                if valor > me['saldo']: st.error("❌ Saldo insuficiente.")
                else:
                    update_saldo(me['id'], -valor); add_tx(me['id'],'boleto','Pagamento de Boleto',valor,'out')
                    st.success(f"✅ Boleto de {fmt(valor)} pago!"); st.rerun()
        with t2:
            pagador = st.text_input("Nome do pagador")
            valor2 = st.number_input("Valor", min_value=0.01, step=10.0, key="boleto_v2")
            desc2 = st.text_input("Descrição")
            if st.button("📄 Gerar Boleto"):
                import random,string
                cod_g = ''.join(random.choices(string.ascii_uppercase+string.digits,k=16))
                st.success(f"📄 Boleto gerado!\nPagador: {pagador}\nValor: {fmt(valor2)}\nCódigo: {cod_g}")

    # ── RECARGA ──
    elif "Recarga" in sel:
        st.markdown("#### 📱 Recarga de Celular")
        op = st.selectbox("Operadora",["Claro","Vivo","TIM","Oi"])
        num = st.text_input("Número do celular")
        valor = st.selectbox("Valor",[10,20,30,50,100])
        if st.button("✅ Recarregar", type="primary"):
            if valor > me['saldo']: st.error("❌ Saldo insuficiente.")
            elif not num: st.error("❌ Informe o número.")
            else:
                update_saldo(me['id'], -valor); add_tx(me['id'],'recarga',f'Recarga {op} {num}',valor,'out')
                st.success(f"✅ Recarga de {fmt(valor)} para {num} ({op})!"); st.rerun()

    # ── CARTÕES ──
    elif "Cartões" in sel:
        st.markdown("#### 💳 Cartões")
        cartoes = me.get('cartoes',[])
        if cartoes:
            for c in cartoes:
                st.markdown(f'<div style="background:linear-gradient(135deg,#1a56db,#0b1f3a);border-radius:14px;padding:20px;margin-bottom:12px;max-width:300px"><div style="font-size:.6rem;color:rgba(255,255,255,.4);margin-bottom:14px">LOGITREIN BANK · {c["tipo"].upper()}</div><div style="font-size:.9rem;letter-spacing:3px;color:rgba(255,255,255,.7);margin-bottom:14px">{c["num"]}</div><div style="font-size:.75rem;color:#fff">{me["nome"][:20].upper()}</div></div>',unsafe_allow_html=True)
        else:
            st.info("Nenhum cartão emitido.")
        col1,col2 = st.columns(2)
        with col1:
            if st.button("+ Cartão Físico"):
                import random
                users=get_users()
                for u in users:
                    if u['id']==me['id']:
                        u.setdefault('cartoes',[]).append({"tipo":"Físico","num":f"**** **** **** {random.randint(1000,9999)}"})
                save_users(users); st.rerun()
        with col2:
            if st.button("+ Cartão Virtual"):
                import random
                users=get_users()
                for u in users:
                    if u['id']==me['id']:
                        u.setdefault('cartoes',[]).append({"tipo":"Virtual","num":f"**** **** **** {random.randint(1000,9999)}"})
                save_users(users); st.rerun()

    # ── CASHBACK ──
    elif "Cashback" in sel:
        st.markdown("#### 🎁 Cashback")
        cb = me.get('cashback',0)
        st.markdown(f'<div class="metric-box"><div class="metric-label">Cashback Disponível</div><div class="metric-value" style="color:#f5c842">{fmt(cb)}</div></div>',unsafe_allow_html=True)
        st.markdown("##### Registrar Compra (ganha 5% cashback)")
        desc_c = st.text_input("Descrição da compra")
        val_c = st.number_input("Valor (R$)", min_value=0.01, step=10.0, key="cb_v")
        if st.button("🛍️ Registrar Compra"):
            if val_c > me['saldo']: st.error("❌ Saldo insuficiente.")
            else:
                cbv = val_c*0.05
                update_saldo(me['id'],-val_c)
                add_tx(me['id'],'compra',desc_c or 'Compra',val_c,'out')
                users=get_users()
                for u in users:
                    if u['id']==me['id']: u['cashback']=float(u.get('cashback',0))+cbv
                save_users(users)
                st.success(f"✅ Compra registrada! Cashback: +{fmt(cbv)}"); st.rerun()
        if cb>0 and st.button("💰 Resgatar Cashback para Conta"):
            update_saldo(me['id'],cb)
            add_tx(me['id'],'cashback','Resgate Cashback',cb,'in')
            users=get_users()
            for u in users:
                if u['id']==me['id']: u['cashback']=0
            save_users(users); st.rerun()

    # ── INVESTIMENTOS ──
    elif "Investimentos" in sel or "Investimento" in sel:
        st.markdown("#### 📈 Investimentos")
        opcoes = {"Poupança (0,5% a.m.)":"poupanca","CDB 110% CDI":"investimentos","Tesouro Direto":"investimentos","LCI/LCA":"investimentos"}
        tipo_inv = st.selectbox("Produto",list(opcoes.keys()))
        val_inv = st.number_input("Valor (R$)", min_value=0.01, step=100.0)
        if st.button("📈 Aplicar", type="primary"):
            if val_inv > me['saldo']: st.error("❌ Saldo insuficiente.")
            else:
                campo = opcoes[tipo_inv]
                update_saldo(me['id'],-val_inv)
                add_tx(me['id'],'investimento',f'Aplicação {tipo_inv}',val_inv,'out')
                users=get_users()
                for u in users:
                    if u['id']==me['id']: u[campo]=float(u.get(campo,0))+val_inv
                save_users(users)
                st.success(f"✅ {fmt(val_inv)} aplicado em {tipo_inv}!"); st.rerun()
        st.markdown("##### Posições")
        c1,c2 = st.columns(2)
        with c1: st.markdown(f'<div class="metric-box"><div class="metric-label">Poupança</div><div class="metric-value" style="color:#00c9a7">{fmt(me.get("poupanca",0))}</div></div>',unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="metric-box"><div class="metric-label">CDB/Tesouro/LCI</div><div class="metric-value" style="color:#93b4f7">{fmt(me.get("investimentos",0))}</div></div>',unsafe_allow_html=True)

    # ── CRÉDITO PF ──
    elif "Crédito" in sel and role=='pf':
        st.markdown("#### 💵 Crédito Pessoal")
        tipo_cred = st.selectbox("Tipo",["Empréstimo Pessoal","Cheque Especial","Consignado"])
        val_cred = st.number_input("Valor (R$)", min_value=100.0, step=100.0)
        prazo = st.selectbox("Prazo",[6,12,18,24,36])
        taxa = 0.029
        if val_cred>0:
            parc = val_cred*taxa/(1-(1+taxa)**(-prazo))
            st.info(f"Parcela estimada: {fmt(parc)}/mês | Total: {fmt(parc*prazo)} | Taxa: 2,9% a.m.")
        if st.button("✅ Solicitar Crédito", type="primary"):
            update_saldo(me['id'],val_cred)
            add_tx(me['id'],'credito',f'{tipo_cred} aprovado',val_cred,'in')
            users=get_users()
            for u in users:
                if u['id']==me['id']: u['dividas']=float(u.get('dividas',0))+val_cred
            save_users(users); st.success(f"✅ {fmt(val_cred)} aprovado e creditado!"); st.rerun()

    # ── CRÉDITO PJ ──
    elif "Crédito" in sel and role=='pj':
        st.markdown("#### 🏦 Crédito Empresarial")
        tipo_cred = st.selectbox("Tipo",["Capital de Giro","Financiamento Equipamentos","Antecipação Recebíveis"])
        val_cred = st.number_input("Valor (R$)", min_value=100.0, step=500.0)
        prazo = st.selectbox("Prazo",[6,12,18,24,36])
        taxa = 0.012
        if val_cred>0:
            parc = val_cred*taxa/(1-(1+taxa)**(-prazo))
            st.info(f"Parcela: {fmt(parc)}/mês | Total: {fmt(parc*prazo)} | Taxa: 1,2% a.m. PJ")
        if st.button("✅ Solicitar", type="primary"):
            update_saldo(me['id'],val_cred)
            add_tx(me['id'],'credito',f'{tipo_cred} aprovado',val_cred,'in')
            users=get_users()
            for u in users:
                if u['id']==me['id']: u['dividas']=float(u.get('dividas',0))+val_cred
            save_users(users); st.success(f"✅ {fmt(val_cred)} aprovado!"); st.rerun()

    # ── FOLHA PJ ──
    elif "Folha" in sel:
        st.markdown("#### 💼 Folha de Pagamento")
        n_func = st.number_input("Nº de funcionários", min_value=1, step=1)
        sal_med = st.number_input("Salário médio (R$)", min_value=0.01, step=100.0)
        if n_func>0 and sal_med>0:
            total = n_func*sal_med; enc = total*0.28
            st.info(f"Salários: {fmt(total)} | Encargos (28%): {fmt(enc)} | Total: {fmt(total+enc)}")
        if st.button("💼 Processar Folha", type="primary"):
            grand = n_func*sal_med*1.28
            if grand>me['saldo']: st.error("❌ Saldo insuficiente.")
            else:
                update_saldo(me['id'],-grand)
                add_tx(me['id'],'folha',f'Folha {n_func} funcionários',grand,'out')
                st.success(f"✅ Folha processada! Total: {fmt(grand)}"); st.rerun()

    # ── FLUXO ──
    elif "Fluxo" in sel:
        st.markdown("#### 🔄 Fluxo de Caixa")
        txs = me.get('transacoes',[])
        ent = sum(t['valor'] for t in txs if t['dir']=='in')
        sai = sum(t['valor'] for t in txs if t['dir']=='out')
        c1,c2,c3 = st.columns(3)
        with c1: st.markdown(f'<div class="metric-box"><div class="metric-label">Entradas</div><div class="metric-value" style="color:#22c55e">{fmt(ent)}</div></div>',unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="metric-box"><div class="metric-label">Saídas</div><div class="metric-value" style="color:#e94b4b">{fmt(sai)}</div></div>',unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="metric-box"><div class="metric-label">Líquido</div><div class="metric-value" style="color:{"#22c55e" if ent-sai>=0 else "#e94b4b"}">{fmt(ent-sai)}</div></div>',unsafe_allow_html=True)
        for tx in txs:
            cor3="#22c55e" if tx['dir']=='in' else "#e94b4b"
            st.markdown(f'<div class="tx-item"><div style="flex:1"><div style="color:#e2ecf8">{tx["desc"]}</div><div style="color:#5a7090;font-size:.7rem">{tx["ts"]}</div></div><div style="color:{cor3};font-weight:700">{"+" if tx["dir"]=="in" else "-"}{fmt(tx["valor"])}</div></div>',unsafe_allow_html=True)

    # ── EXTRATO ──
    elif "Extrato" in sel:
        st.markdown("#### 📋 Extrato Completo")
        txs = me.get('transacoes',[])
        if not txs: st.info("Nenhuma transação ainda.")
        for tx in txs:
            cor3="#22c55e" if tx['dir']=='in' else "#e94b4b"
            st.markdown(f'<div class="tx-item"><div style="flex:1"><div style="color:#e2ecf8">{tx["desc"]}</div><div style="color:#5a7090;font-size:.7rem">{tx["ts"]}</div></div><div style="color:{cor3};font-weight:700">{"+" if tx["dir"]=="in" else "-"}{fmt(tx["valor"])}</div></div>',unsafe_allow_html=True)

    # ── USUÁRIOS (Gerente/CEO) ──
    elif "Usuários" in sel:
        st.markdown("#### 👥 Gerenciar Usuários")
        users = get_users()
        can_edit = [u for u in users if not (me['role']=='gerente' and u['role'] in ['ceo','gerente'])]

        with st.expander("➕ Criar Novo Usuário"):
            c1,c2,c3 = st.columns(3)
            with c1: nu_nome = st.text_input("Nome completo",key="nu_n")
            with c2: nu_login = st.text_input("Login",key="nu_l")
            with c3: nu_senha = st.text_input("Senha",type="password",key="nu_s")
            c4,c5 = st.columns(2)
            with c4:
                roles_disp = ["pf","pj","salario"] if me['role']=='gerente' else ["pf","pj","salario","gerente"]
                nu_role = st.selectbox("Perfil",[ROLE_LABELS[r] for r in roles_disp],key="nu_r")
                nu_role_val = roles_disp[[ROLE_LABELS[r] for r in roles_disp].index(nu_role)]
            with c5: nu_saldo = st.number_input("Saldo inicial (R$)",min_value=0.0,key="nu_sl")
            if st.button("✅ Criar Usuário", type="primary"):
                if not nu_nome or not nu_login or not nu_senha: st.error("Preencha todos os campos.")
                elif any(u['login'].lower()==nu_login.lower() for u in users): st.error("Login já existe!")
                elif len(nu_senha)<4: st.error("Senha mínimo 4 caracteres.")
                else:
                    import random
                    novo = {"id":f"u{len(users)+1}{random.randint(100,999)}","login":nu_login,"senha":nu_senha,"nome":nu_nome,"role":nu_role_val,"agencia":"0001","conta":f"{10000+len(users)}-{random.randint(0,9)}","saldo":float(nu_saldo),"poupanca":0,"investimentos":0,"cashback":0,"dividas":0,"cartoes":[],"transacoes":[],"ativo":True}
                    users.append(novo); save_users(users)
                    st.success(f"✅ Usuário '{nu_nome}' criado! Login: {nu_login}"); st.rerun()

        for u in can_edit:
            cor2=ROLE_CORES.get(u['role'],'#fff')
            c1,c2,c3,c4 = st.columns([3,2,1,1])
            with c1: st.markdown(f"**{u['nome']}** <span style='color:{cor2};font-size:.7rem'>{ROLE_LABELS.get(u['role'],'')}</span> <span style='color:#5a7090;font-size:.7rem'>· {u['login']}</span>",unsafe_allow_html=True)
            with c2: st.markdown(f"<span style='color:#22c55e'>{fmt(u['saldo'])}</span>",unsafe_allow_html=True)
            with c3:
                status = "✅" if u['ativo'] else "❌"
                if st.button(status,key=f"tog_{u['id']}",help="Ativar/Bloquear"):
                    for usr in users:
                        if usr['id']==u['id']: usr['ativo']=not usr['ativo']
                    save_users(users); st.rerun()
            with c4:
                if st.button("💰",key=f"adj_{u['id']}",help="Ajustar saldo"):
                    st.session_state[f'adj_uid']=u['id']
        if st.session_state.get('adj_uid'):
            uid = st.session_state.adj_uid
            u_nome = next((u['nome'] for u in users if u['id']==uid),'')
            adj_val = st.number_input(f"Valor para {u_nome} (negativo = débito)",step=100.0,key="adj_v")
            if st.button("✅ Confirmar Ajuste"):
                update_saldo(uid,adj_val)
                add_tx(uid,'deposito',f'Ajuste por {me["nome"]}',abs(adj_val),'in' if adj_val>=0 else 'out')
                del st.session_state['adj_uid']; st.rerun()

# ══════════════════════════════════════════════
#  ADMIN
# ══════════════════════════════════════════════
elif tela == 'admin':
    if not st.session_state.admin_ok:
        st.markdown("<div style='height:30px'></div>",unsafe_allow_html=True)
        _,col,_ = st.columns([1,1.4,1])
        with col:
            st.markdown('<div style="background:#0f1929;border:1px solid rgba(245,200,66,.2);border-radius:14px;padding:28px;text-align:center"><div style="font-size:2rem">🔐</div><div style="font-family:Syne,sans-serif;color:#f5c842;font-weight:700;margin:8px 0">Área Restrita</div><div style="font-size:.73rem;color:#3a5070">Acesso exclusivo ao proprietário.</div></div>',unsafe_allow_html=True)
            st.markdown("<div style='height:8px'></div>",unsafe_allow_html=True)
            senha=st.text_input("",type="password",placeholder="Senha de administrador",label_visibility="collapsed")
            if st.button("🔓 Entrar",use_container_width=True,type="primary"):
                if checar_admin(senha): st.session_state.admin_ok=True; st.rerun()
                else: st.error("❌ Acesso negado.")
    else:
        st.markdown('<div style="padding:12px 16px;background:#0f1929;border:1px solid rgba(245,200,66,.2);border-radius:10px;margin-bottom:18px"><span style="font-family:Syne,sans-serif;font-size:1rem;font-weight:800;color:#f5c842">⚙️ Painel Administrativo</span> <span style="font-size:.7rem;color:#5a7090">Jorge Zensque — Proprietário</span></div>',unsafe_allow_html=True)
        tab1,tab2 = st.tabs(["📁 Arquivos HTML","🔑 Segurança"])
        with tab1:
            st.caption("Upload de versões novas sem acessar o GitHub.")
            c1,c2=st.columns(2)
            with c1:
                f=lt_file() or 'logitrein.html'
                st.markdown(f"**🏭 Logitrein** `{f}` {'✅ '+get_size(f) if file_exists(f) else '❌'}")
                up=st.file_uploader("Novo Logitrein",type=['html'],key='up_lt')
                if up: (Path(__file__).parent/'logitrein.html').write_bytes(up.read()); st.success("✅ Atualizado!"); st.rerun()
            with c2:
                st.markdown("**🏦 Banco** agora em Python — não precisa de HTML")
                st.info("O banco está integrado neste portal. Use o menu lateral para acessar.")
        with tab2:
            n1=st.text_input("Nova senha admin",type="password",placeholder="Mínimo 8 caracteres")
            n2=st.text_input("Confirmar",type="password")
            if st.button("🔑 Gerar hash"):
                if len(n1)<8: st.error("Mínimo 8 caracteres.")
                elif n1!=n2: st.error("Não conferem.")
                else:
                    h=hashlib.sha256(n1.encode()).hexdigest()
                    st.success("Cole no app.py:")
                    st.code(f'ADMIN_HASH = "{h}"',language="python")
            if st.button("🚪 Sair"): st.session_state.admin_ok=False; st.session_state.tela='portal'; st.rerun()
