import streamlit as st
import streamlit.components.v1 as components
import os

# ══════════════════════════════════════════════════════════════
# LogiTrein 4.0 — Streamlit App
# SEGURANÇA: Área do Educador protegida por senha separada
# Credenciais NUNCA aparecem sem autenticação dupla
# ══════════════════════════════════════════════════════════════

st.set_page_config(
    page_title='LogiTrein 4.0 - Sistema de Gestão',
    layout='wide',
    initial_sidebar_state='collapsed',
    page_icon="🚚"
)

# ── 1. TRAVA DE ACESSO GERAL ──────────────────────────────────
def check_password():
    if "password_correct" not in st.session_state:
        st.markdown("""
        <div style='text-align:center;padding:60px 20px 20px'>
          <div style='font-size:48px'>🚚</div>
          <h1 style='font-family:sans-serif;color:#38bdf8;letter-spacing:-1px'>LOGITREIN 4.0</h1>
          <p style='color:#64748b;font-size:14px'>Sistema de Gestão Operacional — Palmas/TO</p>
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            password = st.text_input("Senha de acesso ao sistema", type="password", placeholder="Digite a senha...")
            if st.button("🔓 Entrar no Sistema", use_container_width=True):
                if password == "jesus@2026":
                    st.session_state["password_correct"] = True
                    st.rerun()
                else:
                    st.error("🚫 Senha incorreta!")
        return False
    return True

if not check_password():
    st.stop()

# ── 2. BLINDAGEM VISUAL ───────────────────────────────────────
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ── 3. CARREGAR LOGITREIN.HTML LOCAL ─────────────────────────
current_dir = os.path.dirname(os.path.abspath(__file__))
html_file = None
for f in sorted(os.listdir(current_dir)):
    if f.lower().endswith('.html'):
        html_file = os.path.join(current_dir, f)
        break

if html_file:
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_data = f.read()
        components.html(html_data, height=900, scrolling=True)
    except Exception as e:
        st.error(f"Erro ao carregar o sistema: {e}")
        st.stop()
else:
    st.error("❌ Arquivo logitrein.html não encontrado no repositório.")
    st.info("Suba o arquivo logitrein.html no mesmo repositório que este app.py.")
    st.stop()

# ── 4. ÁREA DO EDUCADOR — SENHA SEPARADA ─────────────────────
st.divider()

with st.expander("🔑 Área do Educador (Coordenação)"):
    if not st.session_state.get("educador_ok", False):
        # PORTÃO: só mostra aviso, pede senha
        st.warning("⚠️ Área exclusiva do coordenador do projeto. Jovens aprendizes não têm acesso.")
        edu_pass = st.text_input(
            "Senha do educador",
            type="password",
            placeholder="Senha do educador...",
            key="edu_pass_input",
            label_visibility="collapsed"
        )
        if st.button("Acessar área do educador", key="btn_edu"):
            if edu_pass == "educador2026":
                st.session_state["educador_ok"] = True
                st.rerun()
            else:
                st.error("Senha incorreta.")
    else:
        # ÁREA DESBLOQUEADA — conteúdo protegido
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🔒 Sair", key="btn_sair_edu"):
                st.session_state["educador_ok"] = False
                st.rerun()
        with col1:
            st.success("✅ Acesso autorizado — Coordenador do Projeto")

        st.markdown("### 📋 Credenciais do Sistema")
        st.markdown("""
| Nível | Usuário | Senha | Perfil |
|:---|:---|:---|:---|
| **Conselho** | `jorge.zensque` | `master2026` | Admin Total |
| **Gestão** | `gestor` | `gest123` | Supervisor |
| **Líderes** | `lider.a` / `lider.b` / `lider.c` | `lid123` | Chefia de Turno |
| **Dep. Pessoal** | `coord.dp` | `dp2026` | Coordenador DP |
| **Operação** | `op01` até `op15` | `op123` | Jovens Aprendizes |
""")
        st.markdown("---")
        st.caption("🔐 Senhas internas do sistema (LogiTrein): Área do Educador = `educador2026` · Credenciais admin = `master2026`")
        st.info("💡 Guarde estas senhas em local seguro. Não compartilhe com os jovens.")
