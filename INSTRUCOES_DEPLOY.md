# 🎯 INSTRUÇÕES ESPECÍFICAS PARA SEU PROJETO

## 📍 Seu Repositório GitHub
**URL:** https://github.com/Gms006/Controle-de-Processos

---

## ⚡ PRIMEIRO TESTE LOCAL (Agora mesmo!)

### **1. Instalar dependências:**
```powershell
cd "c:\acessorias processos\streamlit_app"
pip install -r requirements.txt
```

### **2. Criar arquivo de secrets:**

Crie o arquivo: `c:\acessorias processos\.streamlit\secrets.toml`

Cole este conteúdo (SUBSTITUA o token):
```toml
[api]
ACESSORIAS_API_TOKEN = "COLE_SEU_TOKEN_AQUI"
ACESSORIAS_API_URL = "https://api.acessorias.com"
```

### **3. Executar o dashboard:**
```powershell
streamlit run app.py
```

O navegador abrirá automaticamente em `http://localhost:8501`

### **4. Fazer primeira sincronização:**
- No dashboard, clique no menu lateral em **"⚙️ Sincronização"**
- Clique no botão **"🚀 Iniciar Sincronização"**
- Aguarde 1-3 minutos
- Volte para **"🏠 Home"** e veja os dados!

---

## 🌐 DEPLOY NO STREAMLIT CLOUD

### **Passo 1: Fazer commit dos arquivos**

```powershell
cd "c:\acessorias processos"

# Adicionar todos os arquivos
git add .

# Commit
git commit -m "✨ Adicionar Dashboard Streamlit completo"

# Push para GitHub
git push origin main
```

### **Passo 2: Acessar Streamlit Cloud**

1. Acesse: https://share.streamlit.io
2. Clique em **"Sign in with GitHub"**
3. Autorize o Streamlit a acessar seu GitHub

### **Passo 3: Criar novo app**

1. Clique em **"New app"**
2. Preencha:
   - **Repository:** selecione `Gms006/Controle-de-Processos`
   - **Branch:** `main`
   - **Main file path:** `streamlit_app/app.py`

### **Passo 4: Configurar Secrets**

1. Clique em **"Advanced settings..."**
2. Na seção **"Secrets"**, cole:

```toml
[api]
ACESSORIAS_API_TOKEN = "COLE_SEU_TOKEN_REAL_AQUI"
ACESSORIAS_API_URL = "https://api.acessorias.com"
```

3. Clique em **"Deploy!"**

### **Passo 5: Aguardar deploy**

- O deploy leva ~2-3 minutos
- Você verá logs em tempo real
- Quando aparecer **"Your app is live!"**, está pronto!

**URL do seu app:** `https://controle-de-processos-gms.streamlit.app`  
*(ou similar - o Streamlit gera automaticamente)*

---

## 🔄 ATIVAR SINCRONIZAÇÃO AUTOMÁTICA

### **Configurar GitHub Secrets:**

1. Acesse: https://github.com/Gms006/Controle-de-Processos/settings/secrets/actions

2. Clique em **"New repository secret"**

3. Adicione o primeiro secret:
   - **Name:** `ACESSORIAS_API_TOKEN`
   - **Secret:** Cole seu token da API
   - Clique em **"Add secret"**

4. Adicione o segundo secret:
   - **Name:** `ACESSORIAS_API_URL`
   - **Secret:** `https://api.acessorias.com`
   - Clique em **"Add secret"**

### **Ativar GitHub Actions:**

1. Acesse: https://github.com/Gms006/Controle-de-Processos/actions

2. Se aparecer botão verde **"I understand my workflows, go ahead and enable them"**, clique nele

3. O workflow será executado automaticamente:
   - **Primeira vez:** Manualmente (próximo passo)
   - **Depois:** A cada 6 horas automaticamente

### **Executar primeira sincronização:**

1. Vá em: https://github.com/Gms006/Controle-de-Processos/actions

2. Clique em **"🔄 Sincronização Automática de Dados"** (esquerda)

3. Clique em **"Run workflow"** (direita)

4. Selecione branch `main` e clique em **"Run workflow"**

5. Aguarde ~2-3 minutos

6. Quando ficar verde ✅, significa que deu certo!

7. O Streamlit Cloud detectará a mudança e atualizará automaticamente

---

## 📊 ESTRUTURA DE DADOS

### **Banco de dados criado automaticamente:**
`streamlit_app/data/processos.db`

### **Tabelas:**
- `empresas` - Cadastro de empresas
- `processos` - Todos os processos
- `passos` - Passos de cada processo
- `desdobramentos` - Desdobramentos/perguntas
- `sincronizacoes` - Histórico de atualizações

### **Regimes sincronizados:**
- Simples Nacional
- Lucro Presumido - Serviços
- Lucro Presumido - Comércio
- Lucro Real - Serviços
- Lucro Real - Comércio

---

## 🎯 FLUXO COMPLETO DE ATUALIZAÇÃO

```
┌─────────────────────────────────────┐
│  GitHub Actions (a cada 6 horas)    │
│  ou Sincronização Manual            │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Busca dados da API Acessórias      │
│  (Processos de todos os regimes)    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Atualiza processos.db              │
│  (Apenas mudanças - incremental)    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Commit automático para GitHub      │
│  (Actions) ou manual (Dashboard)    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Streamlit Cloud detecta mudança    │
│  e atualiza o dashboard             │
└─────────────────────────────────────┘
```

---

## ✅ CHECKLIST DE IMPLEMENTAÇÃO

### **Teste Local:**
- [ ] Instalou dependências (`pip install -r requirements.txt`)
- [ ] Criou arquivo `.streamlit/secrets.toml` com seu token
- [ ] Executou `streamlit run app.py`
- [ ] Fez primeira sincronização no dashboard
- [ ] Visualizou dados em todas as páginas

### **Deploy Online:**
- [ ] Fez commit e push para GitHub
- [ ] Criou app no Streamlit Cloud
- [ ] Configurou secrets no Streamlit Cloud
- [ ] App está online e acessível

### **Automação:**
- [ ] Configurou secrets no GitHub Actions
- [ ] Ativou workflows
- [ ] Executou primeira sincronização via Actions
- [ ] Confirmou que banco foi atualizado

---

## 🆘 TROUBLESHOOTING

### **Erro: "No module named 'streamlit'"**
```powershell
pip install streamlit pandas plotly requests sqlalchemy
```

### **Dashboard não abre:**
- Certifique-se de estar na pasta correta: `cd streamlit_app`
- Verifique se a porta 8501 está livre

### **Erro de token inválido:**
- Verifique se copiou o token corretamente
- Teste o token diretamente na API Acessórias

### **Banco vazio no deploy:**
- Execute a sincronização manualmente na página ⚙️
- Ou rode o GitHub Actions workflow

### **GitHub Actions falha:**
- Verifique se os secrets estão configurados
- Veja os logs detalhados na aba Actions

---

## 📞 RECURSOS ÚTEIS

**Seu Repositório:**  
https://github.com/Gms006/Controle-de-Processos

**Streamlit Cloud:**  
https://share.streamlit.io

**Documentação:**  
- `streamlit_app/README.md` - Documentação completa
- `streamlit_app/QUICK_START.md` - Guia rápido
- `RESUMO_IMPLEMENTACAO_STREAMLIT.md` - Este arquivo

---

## 🎉 PRONTO PARA USAR!

Agora você tem:

✅ **Dashboard local** funcionando  
✅ **Deploy online** no Streamlit Cloud  
✅ **Atualização automática** a cada 6 horas  
✅ **Acesso de qualquer lugar**  
✅ **Dados sempre atualizados**  
✅ **100% gratuito**  

**Aproveite seu novo sistema de gestão de processos!** 🚀
