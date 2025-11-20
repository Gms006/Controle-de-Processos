# 📊 Dashboard Streamlit - Gestão de Processos Contábeis

Sistema web interativo para acompanhamento de processos contábeis da API Acessórias.

## 🎯 Características

✅ **Dashboard Interativo** - Visualização em tempo real de métricas e KPIs  
✅ **Análise de Processos** - Filtros avançados e tabelas dinâmicas  
✅ **Análise de Empresas** - Rankings e comparativos de performance  
✅ **Sincronização Automática** - Atualização programada via GitHub Actions  
✅ **100% Gratuito** - Deploy no Streamlit Cloud sem custos  

---

## 🚀 Deploy no Streamlit Cloud

### **Passo 1: Preparar o Repositório GitHub**

1. Faça commit de todos os arquivos do projeto:
```powershell
cd "c:\acessorias processos"
git add .
git commit -m "✨ Adicionar dashboard Streamlit"
git push origin main
```

2. Verifique se o repositório está correto: `https://github.com/Gms006/Controle-de-Processos`

### **Passo 2: Configurar Secrets Localmente (Teste)**

Crie o arquivo `.streamlit/secrets.toml` (NÃO commitar!):

```toml
[api]
ACESSORIAS_API_TOKEN = "seu_token_aqui"
ACESSORIAS_API_URL = "https://api.acessorias.com"
```

### **Passo 3: Testar Localmente**

```powershell
cd "c:\acessorias processos\streamlit_app"
pip install -r requirements.txt
streamlit run app.py
```

Acesse: `http://localhost:8501`

### **Passo 4: Deploy no Streamlit Cloud**

1. Acesse: https://streamlit.io/cloud
2. Faça login com sua conta GitHub
3. Clique em **"New app"**
4. Configure:
   - **Repository:** `Gms006/Controle-de-Processos`
   - **Branch:** `main`
   - **Main file path:** `streamlit_app/app.py`
5. Clique em **"Advanced settings"**
6. Em **"Secrets"**, cole:

```toml
[api]
ACESSORIAS_API_TOKEN = "seu_token_real_aqui"
ACESSORIAS_API_URL = "https://api.acessorias.com"
```

7. Clique em **"Deploy!"**

**URL do seu app:** `https://controle-processos-gms.streamlit.app`

---

## 🔄 Configurar Sincronização Automática (GitHub Actions)

### **Passo 1: Configurar Secrets no GitHub**

1. Acesse: `https://github.com/Gms006/Controle-de-Processos/settings/secrets/actions`
2. Clique em **"New repository secret"**
3. Adicione os seguintes secrets:

| Nome | Valor |
|------|-------|
| `ACESSORIAS_API_TOKEN` | Seu token da API Acessórias |
| `ACESSORIAS_API_URL` | `https://api.acessorias.com` |

### **Passo 2: Ativar GitHub Actions**

1. Acesse a aba **"Actions"** do repositório
2. Clique em **"I understand my workflows, go ahead and enable them"**
3. O workflow `sync-data.yml` será executado automaticamente a cada 6 horas

### **Passo 3: Executar Sincronização Manual**

1. Vá em **Actions** > **"🔄 Sincronização Automática de Dados"**
2. Clique em **"Run workflow"**
3. Aguarde a conclusão (1-3 minutos)

---

## 📁 Estrutura do Projeto

```
streamlit_app/
├── app.py                          # Aplicação principal (Home)
├── pages/
│   ├── 1_📋_Processos.py           # Análise de processos
│   ├── 2_🏢_Empresas.py            # Análise de empresas
│   └── 3_⚙️_Sincronização.py      # Gerenciamento de sync
├── components/
│   ├── metrics.py                  # Componentes de métricas/KPIs
│   ├── charts.py                   # Gráficos (Plotly)
│   └── filters.py                  # Filtros interativos
├── utils/
│   ├── database.py                 # Gerenciador SQLite
│   ├── sync_manager.py             # Sincronização com API
│   └── formatters.py               # Formatadores de dados
├── data/
│   └── processos.db                # Banco SQLite (gerado automaticamente)
└── requirements.txt                # Dependências Python
```

---

## 🔧 Comandos Úteis

### **Executar Localmente**
```powershell
cd "c:\acessorias processos\streamlit_app"
streamlit run app.py
```

### **Sincronizar Dados Manualmente**
```powershell
cd "c:\acessorias processos"
python .github/workflows/sync_script.py
```

### **Limpar Cache do Streamlit**
Pressione `C` no navegador enquanto o app estiver rodando

### **Atualizar Dependências**
```powershell
pip install -r streamlit_app/requirements.txt --upgrade
```

---

## 📊 Funcionalidades

### **🏠 Dashboard Principal (Home)**
- 📈 KPIs principais (Total, Concluídos, Em Andamento)
- 📊 Gráficos de distribuição por status e regime
- ⚠️ Alertas de processos parados
- 📋 Lista de processos recentes

### **📋 Página de Processos**
- 🔍 Filtros avançados (competência, regime, status, busca)
- 📊 Top 10 empresas com mais processos
- 📋 Tabela interativa com todos os processos
- 📥 Download em CSV
- 🔍 Detalhes de passos por processo

### **🏢 Página de Empresas**
- 🏆 Rankings (mais rápidas / mais lentas)
- 📊 Análise de performance por empresa
- 💼 Distribuição por regime tributário
- 🔍 Detalhes dos processos por empresa

### **⚙️ Página de Sincronização**
- 📊 Status da última atualização
- 🔄 Sincronização manual sob demanda
- 📜 Histórico de sincronizações
- ℹ️ Informações e estatísticas

---

## 🔐 Segurança

✅ **Secrets protegidos** - Nunca são commitados no Git  
✅ **Repositório privado** - Código-fonte protegido  
✅ **App público** - Dashboard acessível via URL  
✅ **HTTPS** - Comunicação criptografada  
✅ **Cache inteligente** - Apenas leitura do banco  

---

## ⚡ Performance

✅ **Cache de 5 minutos** - Reduz consultas ao banco  
✅ **Índices otimizados** - Queries rápidas no SQLite  
✅ **Sincronização incremental** - Apenas mudanças são atualizadas  
✅ **Lazy loading** - Dados carregados sob demanda  

---

## 🆘 Troubleshooting

### **Erro: "No module named 'streamlit'"**
```powershell
pip install -r streamlit_app/requirements.txt
```

### **Erro: "ACESSORIAS_API_TOKEN não configurado"**
- Verifique se criou o arquivo `.streamlit/secrets.toml`
- No Streamlit Cloud, verifique se adicionou os secrets

### **Banco de dados vazio**
- Execute a sincronização na página "⚙️ Sincronização"
- Ou rode: `python .github/workflows/sync_script.py`

### **GitHub Actions não executa**
- Verifique se os secrets estão configurados no GitHub
- Acesse Actions > Habilite workflows

---

## 📞 Suporte

**Documentação Streamlit:** https://docs.streamlit.io  
**Streamlit Cloud:** https://streamlit.io/cloud  
**GitHub Actions:** https://docs.github.com/actions  

---

## 📝 Changelog

### v1.0.0 (Novembro 2025)
- ✨ Dashboard inicial com 3 páginas
- 🔄 Sincronização automática via GitHub Actions
- 📊 Gráficos interativos com Plotly
- 🔍 Filtros avançados e buscas
- 📥 Export para CSV
- ⚡ Cache inteligente

---

## 📄 Licença

Este projeto é de uso interno. Todos os direitos reservados.

---

<div align="center">
  
**📊 Dashboard de Gestão de Processos Contábeis**  
*Desenvolvido com Streamlit | Novembro 2025*

</div>
