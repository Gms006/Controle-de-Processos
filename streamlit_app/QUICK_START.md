# 🚀 GUIA RÁPIDO - Começar em 5 Minutos

## 📋 Pré-requisitos
- ✅ Python 3.8+ instalado
- ✅ Conta no GitHub
- ✅ Token da API Acessórias

---

## ⚡ Início Rápido

### **1️⃣ Instalar Dependências (1 min)**

```powershell
cd "c:\acessorias processos\streamlit_app"
pip install -r requirements.txt
```

### **2️⃣ Configurar Secrets (1 min)**

Crie o arquivo `.streamlit/secrets.toml`:

```toml
[api]
ACESSORIAS_API_TOKEN = "SEU_TOKEN_AQUI"
ACESSORIAS_API_URL = "https://api.acessorias.com"
```

### **3️⃣ Executar o Dashboard (30 seg)**

```powershell
streamlit run app.py
```

Abra: http://localhost:8501

### **4️⃣ Sincronizar Dados (2 min)**

No dashboard:
1. Acesse a página **⚙️ Sincronização**
2. Clique em **"🚀 Iniciar Sincronização"**
3. Aguarde a conclusão

✅ **Pronto!** Agora você tem acesso a todos os dados!

---

## 🌐 Deploy Online (5 min)

### **Passo 1: Push para GitHub**

```powershell
cd "c:\acessorias processos"
git add .
git commit -m "✨ Dashboard Streamlit completo"
git push origin main
```

### **Passo 2: Deploy no Streamlit Cloud**

1. Acesse: https://share.streamlit.io
2. Conecte seu GitHub
3. Selecione:
   - **Repo:** `Gms006/Controle-de-Processos`
   - **Branch:** `main`
   - **File:** `streamlit_app/app.py`
4. Cole seus secrets
5. **Deploy!**

**Seu app estará online em ~3 minutos!** 🎉

---

## 🔄 Sincronização Automática (GitHub Actions)

### **Configurar Secrets no GitHub:**

1. Vá em: `Settings > Secrets and variables > Actions`
2. Adicione:
   - `ACESSORIAS_API_TOKEN` = seu_token
   - `ACESSORIAS_API_URL` = https://api.acessorias.com

### **Ativar Actions:**

1. Acesse a aba **Actions**
2. Habilite workflows
3. Pronto! Dados serão atualizados a cada 6 horas automaticamente

---

## 📊 Páginas Disponíveis

| Página | Descrição |
|--------|-----------|
| 🏠 **Home** | Dashboard com KPIs e métricas gerais |
| 📋 **Processos** | Lista completa com filtros avançados |
| 🏢 **Empresas** | Análise de performance por empresa |
| ⚙️ **Sincronização** | Atualizar dados manualmente |

---

## 💡 Dicas

✅ **Cache:** Dados são cacheados por 5 minutos para performance  
✅ **Filtros:** Use a sidebar para filtrar por competência/regime  
✅ **Download:** Baixe relatórios em CSV nas páginas  
✅ **Mobile:** Dashboard 100% responsivo  

---

## 🆘 Problemas Comuns

### **Erro ao importar módulos**
```powershell
pip install -r requirements.txt --upgrade
```

### **Secrets não encontrados**
- Verifique se criou `.streamlit/secrets.toml`
- Certifique-se de que está no formato TOML correto

### **Banco vazio**
- Execute a sincronização primeiro na página ⚙️

---

## ✅ Checklist Final

- [ ] Python 3.8+ instalado
- [ ] Dependências instaladas
- [ ] Arquivo secrets.toml criado
- [ ] Dashboard rodando localmente
- [ ] Primeira sincronização concluída
- [ ] Push para GitHub
- [ ] Deploy no Streamlit Cloud
- [ ] Secrets configurados no GitHub
- [ ] GitHub Actions ativado

---

<div align="center">

**🎉 Parabéns! Seu dashboard está pronto!**

**URL Local:** http://localhost:8501  
**URL Online:** https://seu-app.streamlit.app

</div>
