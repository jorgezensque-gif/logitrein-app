"""
╔══════════════════════════════════════════════════════════════╗
║         LOGITREIN + BANCO — SERVIDOR STREAMLIT               ║
║  Gerencia acesso unificado ao Logitrein v12 e Banco Digital  ║
╚══════════════════════════════════════════════════════════════╝

Uso:
    pip install streamlit
    streamlit run app.py

Ou via requirements.txt:
    pip install -r requirements.txt
    streamlit run app.py
"""

import streamlit as st
import json
import os
import base64
from pathlib import Path
from datetime import datetime

# ──────────────────────────────────────────────
#  CONFIGURAÇÃO DA PÁGINA
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Logitrein — Portal de Acesso",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ──────────────────────────────────────────────
#  CSS GLOBAL
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background: #09182e !important;
    color: #ddeaf8;
}
.main { background: #09182e !important; }
.block-container { padding: 2rem 2rem 1rem !important; max-width: 1100px; }

h1, h2, h3 { font-family: 'Syne', sans-serif !important; }

/* Cards */
.lt-card {
    background: #132240;
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 14px;
    padding: 28px 24px;
    margin-bottom: 16px;
    transition: border-color .2s;
}
.lt-card:hover { border-color: rgba(0,201,167,.3); }

.lt-card-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    margin-bottom: 8px;
    color: #fff;
}
.lt-card-desc {
    font-size: .85rem;
    color: #7a9bbf;
    line-height: 1.6;
    margin-bottom: 16px;
}

/* Badges */
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 99px;
    font-size: .65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .8px;
    margin-left: 8px;
}
.badge-teal { background: rgba(0,201,167,.15); color: #00c9a7; }
.badge-gold { background: rgba(245,200,66,.15); color: #f5c842; }
.badge-blue { background: rgba(26,86,219,.2); color: #93b4f7; }

/* Banner */
.lt-banner {
    background: linear-gradient(135deg, #112240 0%, #0d2a55 100%);
    border: 1px solid rgba(0,201,167,.15);
    border-radius: 16px;
    padding: 32px 36px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.lt-banner::before {
    content: '';
    position: absolute;
    right: -40px; top: -40px;
    width: 220px; height: 220px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(0,201,167,.08) 0%, transparent 70%);
}
.lt-brand {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #00c9a7;
    margin-bottom: 4px;
}
.lt-brand span { color: #f5c842; }
.lt-subtitle { font-size: .9rem; color: #7a9bbf; }

/* Info boxes */
.info-box {
    background: rgba(0,201,167,.07);
    border: 1px solid rgba(0,201,167,.18);
    border-radius: 10px;
    padding: 12px 16px;
    font-size: .82rem;
    color: #6ee7da;
    margin: 10px 0;
    line-height: 1.6;
}
.warn-box {
    background: rgba(245,200,66,.07);
    border: 1px solid rgba(245,200,66,.2);
    border-radius: 10px;
    padding: 12px 16px;
    font-size: .82rem;
    color: #fde68a;
    margin: 10px 0;
    line-height: 1.6;
}

/* Metric mini */
.mini-metric {
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 10px;
    padding: 14px;
    text-align: center;
}
.mini-label { font-size: .65rem; color: #7a9bbf; text-transform: uppercase; letter-spacing: .8px; }
.mini-val { font-family: 'Syne', sans-serif; font-size: 1.3rem; font-weight: 700; }

/* Hide streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Iframe container */
.iframe-container {
    width: 100%;
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 14px;
    overflow: hidden;
    background: #09182e;
}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
#  FUNÇÕES AUXILIARES
# ──────────────────────────────────────────────
def load_html_file(filename: str) -> str:
    """Carrega arquivo HTML do diretório atual."""
    path = Path(__file__).parent / filename
    if path.exists():
        return path.read_text(encoding='utf-8')
    return None

def get_file_as_base64(filename: str) -> str:
    """Converte HTML para base64 para embed via iframe."""
    html = load_html_file(filename)
    if html:
        b64 = base64.b64encode(html.encode('utf-8')).decode()
        return f"data:text/html;base64,{b64}"
    return None

def file_exists(filename: str) -> bool:
    return (Path(__file__).parent / filename).exists()

def get_file_size(filename: str) -> str:
    path = Path(__file__).parent / filename
    if path.exists():
        size = path.stat().st_size
        if size > 1024*1024:
            return f"{size/1024/1024:.1f} MB"
        return f"{size/1024:.0f} KB"
    return "—"

# ──────────────────────────────────────────────
#  ESTADO DA SESSÃO
# ──────────────────────────────────────────────
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'portal'

# ──────────────────────────────────────────────
#  PORTAL PRINCIPAL
# ──────────────────────────────────────────────
def pagina_portal():
    # Banner
    st.markdown("""
    <div class="lt-banner">
        <div class="lt-brand">🏭 Logit<span>rein</span> · 🏦 Banco</div>
        <div class="lt-subtitle">Portal integrado de gestão logística e financeira</div>
    </div>
    """, unsafe_allow_html=True)

    # Status dos arquivos
    logitrein_ok = file_exists('logitrein.html') or file_exists('logitrein_v12_integrado.html')
    banco_ok = file_exists('logitrein_banco_v2.html') or file_exists('banco.html')

    logitrein_file = 'logitrein_v12_integrado.html' if file_exists('logitrein_v12_integrado.html') else 'logitrein.html'
    banco_file = 'logitrein_banco_v2.html' if file_exists('logitrein_banco_v2.html') else 'banco.html'

    # Métricas
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="mini-metric">
            <div class="mini-label">Logitrein v12</div>
            <div class="mini-val" style="color:{'#22c55e' if logitrein_ok else '#e94b4b'}">
                {'✅ Online' if logitrein_ok else '❌ Faltando'}
            </div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="mini-metric">
            <div class="mini-label">Banco Logitrein</div>
            <div class="mini-val" style="color:{'#22c55e' if banco_ok else '#e94b4b'}">
                {'✅ Online' if banco_ok else '❌ Faltando'}
            </div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="mini-metric">
            <div class="mini-label">Logitrein</div>
            <div class="mini-val" style="color:#7a9bbf;font-size:.9rem">{get_file_size(logitrein_file)}</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="mini-metric">
            <div class="mini-label">Banco</div>
            <div class="mini-val" style="color:#7a9bbf;font-size:.9rem">{get_file_size(banco_file)}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Cards de acesso
    col_a, col_b = st.columns(2, gap="large")

    with col_a:
        st.markdown("""
        <div class="lt-card">
            <div class="lt-card-title">
                🏭 Logitrein v12
                <span class="badge badge-blue">Logística</span>
            </div>
            <div class="lt-card-desc">
                Sistema de gestão logística completo. Controle de equipes, ponto eletrônico,
                DP com folha de pagamento, banco de horas e integração com o Banco Logitrein.
            </div>
            <div style="font-size:.75rem;color:#4a6080;margin-bottom:6px">
                Acesse com suas credenciais fornecidas pelo coordenador.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Abrir Logitrein v12", key="btn_logitrein", use_container_width=True,
                     disabled=not logitrein_ok):
            st.session_state.pagina = 'logitrein'
            st.rerun()

    with col_b:
        st.markdown("""
        <div class="lt-card">
            <div class="lt-card-title">
                🏦 Banco Logitrein
                <span class="badge badge-teal">Financeiro</span>
            </div>
            <div class="lt-card-desc">
                Banco digital completo. Conta corrente, Pix, transferências, investimentos,
                crédito, bolsa de valores e recebimento automático de folha de pagamento.
            </div>
            <div style="font-size:.75rem;color:#4a6080;margin-bottom:6px">
                Acesse com suas credenciais fornecidas pelo gerente da agência.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🏦 Abrir Banco Logitrein", key="btn_banco", use_container_width=True,
                     disabled=not banco_ok):
            st.session_state.pagina = 'banco'
            st.rerun()

    # Info de integração
    st.markdown("""
    <div class="info-box">
        🔗 <strong>Integração Automática:</strong> Quando o DP do Logitrein fecha uma folha de pagamento,
        os salários são depositados automaticamente nas contas salário do Banco Logitrein
        (compartilham o mesmo <code>localStorage</code> do navegador).
    </div>
    <div class="warn-box">
        ⚠️ <strong>Importante:</strong> Para a integração funcionar, o Logitrein e o Banco precisam estar
        abertos na <strong>mesma aba do navegador</strong> (use os botões acima ou o menu lateral).
        Arquivos abertos em abas separadas também funcionam se forem do mesmo domínio/origem.
    </div>
    """, unsafe_allow_html=True)

    # Guia de uso rápido
    with st.expander("📖 Guia de Uso — Como usar os dois sistemas juntos"):
        st.markdown("""
        ### 1️⃣ Abrir os dois sistemas
        Use os botões acima ou o menu lateral para navegar entre o Logitrein e o Banco.
        Ambos ficam embarcados aqui no portal Streamlit.

        ### 2️⃣ Logitrein → DP → Folha de Pagamento
        1. Entre no Logitrein com suas credenciais de coordenador
        2. Vá em **DP** → **Folha de Pagamento**
        3. Selecione o mês e clique em **Calcular Folha**
        4. Clique em **✓ Fechar Folha**
        5. O sistema automaticamente deposita os salários no banco!

        ### 3️⃣ Banco → Conferir depósitos
        1. Entre no Banco com suas credenciais de gerente ou CEO
        2. Clique em **💼 Folha → Banco** no menu lateral
        3. Veja as folhas processadas e os depósitos realizados
        4. Funcionários com Conta Salário recebem os valores automaticamente

        ### 4️⃣ Criar contas para funcionários
        - No Banco, como Gerente ou CEO, vá em **👥 Gerenciar Usuários**
        - Clique em **+ Novo Usuário** → escolha perfil **Conta Salário**
        - O nome deve ser **idêntico** ao cadastrado no Logitrein para o depósito automático

        ### 🔑 Credenciais de Acesso
        Os logins e senhas são fornecidos pelo **coordenador** (Logitrein)
        ou pelo **gerente da agência** (Banco). Entre em contato com o responsável
        para obter suas credenciais de acesso.
        """)




# ──────────────────────────────────────────────
#  PÁGINA LOGITREIN
# ──────────────────────────────────────────────
def pagina_logitrein():
    col_back, col_title = st.columns([1, 6])
    with col_back:
        if st.button("← Portal", key="back_lt"):
            st.session_state.pagina = 'portal'
            st.rerun()
    with col_title:
        st.markdown("<h2 style='margin:0;font-family:Syne,sans-serif;color:#38bdf8'>🏭 Logitrein v12</h2>", unsafe_allow_html=True)

    logitrein_file = 'logitrein_v12_integrado.html' if file_exists('logitrein_v12_integrado.html') else 'logitrein.html'
    data_url = get_file_as_base64(logitrein_file)

    if data_url:
        st.markdown(f"""
        <div class="iframe-container">
            <iframe src="{data_url}"
                width="100%" height="900"
                frameborder="0"
                style="display:block">
            </iframe>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error(f"Arquivo `{logitrein_file}` não encontrado. Faça o upload no portal.")


# ──────────────────────────────────────────────
#  PÁGINA BANCO
# ──────────────────────────────────────────────
def pagina_banco():
    col_back, col_title = st.columns([1, 6])
    with col_back:
        if st.button("← Portal", key="back_banco"):
            st.session_state.pagina = 'portal'
            st.rerun()
    with col_title:
        st.markdown("<h2 style='margin:0;font-family:Syne,sans-serif;color:#00c9a7'>🏦 Banco Logitrein</h2>", unsafe_allow_html=True)

    banco_file = 'logitrein_banco_v2.html' if file_exists('logitrein_banco_v2.html') else 'banco.html'
    data_url = get_file_as_base64(banco_file)

    if data_url:
        st.markdown(f"""
        <div class="iframe-container">
            <iframe src="{data_url}"
                width="100%" height="900"
                frameborder="0"
                style="display:block">
            </iframe>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error(f"Arquivo `{banco_file}` não encontrado. Faça o upload no portal.")


# ──────────────────────────────────────────────
#  SIDEBAR NAVEGAÇÃO
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:800;color:#00c9a7;padding:10px 0 16px">
        🏦 Logitrein Portal
    </div>
    """, unsafe_allow_html=True)

    if st.button("🏠 Portal Principal", use_container_width=True):
        st.session_state.pagina = 'portal'
        st.rerun()

    if st.button("🏭 Logitrein v12", use_container_width=True,
                 disabled=not (file_exists('logitrein_v12_integrado.html') or file_exists('logitrein.html'))):
        st.session_state.pagina = 'logitrein'
        st.rerun()

    if st.button("🏦 Banco Logitrein", use_container_width=True,
                 disabled=not (file_exists('logitrein_banco_v2.html') or file_exists('banco.html'))):
        st.session_state.pagina = 'banco'
        st.rerun()

    st.divider()
    st.markdown(f"<div style='font-size:.7rem;color:#475569'>Logitrein Portal v2.0<br>{datetime.now().strftime('%d/%m/%Y %H:%M')}</div>", unsafe_allow_html=True)


# ──────────────────────────────────────────────
#  ROTEADOR
# ──────────────────────────────────────────────
if st.session_state.pagina == 'portal':
    pagina_portal()
elif st.session_state.pagina == 'logitrein':
    pagina_logitrein()
elif st.session_state.pagina == 'banco':
    pagina_banco()
