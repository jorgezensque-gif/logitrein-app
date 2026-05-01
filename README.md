# 🏦 Logitrein Portal v7.0

Portal integrado com sistema de gestão operacional (Logitrein v12) e banco digital (Logitrein Bank).

## 📁 Estrutura do repositório

```
logitrein-app/
├── app.py               # Portal Streamlit principal
├── requirements.txt     # Dependências
├── logitrein.html       # Sistema Logitrein v12 (gestão operacional)
└── README.md
```

> ⚠️ O arquivo `logitrein_banco_v2.html` **não é necessário** — o banco está integrado no `app.py`.

## 🚀 Deploy no Streamlit Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Conecte ao repositório `jorgezensque-gif/logitrein-app`
3. Main file: `app.py`
4. Clique em **Deploy**

## 🔑 Credenciais padrão

### Logitrein v12 (gestão)
Conforme configurado no `logitrein.html`.

### Banco Logitrein
| Login | Senha | Perfil |
|-------|-------|--------|
| ceo | ceo123 | CEO |
| gerente1 | ger123 | Gerente |
| joao.silva | 123456 | Pessoa Física |
| emp.ltda | empresa1 | Pessoa Jurídica |
| maria.santos | salario1 | Conta Salário |

### Admin Portal
Senha configurada no `app.py` (`ADMIN_HASH`).

## 🔗 Integração Logitrein → Banco

Ao fechar a folha de pagamento no Logitrein v12, os salários são depositados automaticamente nas contas salário do Banco via `postMessage` + `query_params`.

## 🏃 Rodar localmente

```bash
pip install streamlit
streamlit run app.py
```
