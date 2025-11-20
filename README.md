# 📊 Dashboard de Controle de Processos Contábeis

Dashboard interativo desenvolvido com **Streamlit** para acompanhamento e gestão de processos contábeis integrado com a API Acessórias.

## 🚀 Funcionalidades

- **Dashboard Principal**: Visão geral com 8 KPIs principais
- **Análise de Processos**: Filtros avançados, exportação CSV, análise de gargalos
- **Gestão de Empresas**: Rankings, performance por regime tributário
- **Sincronização Automática**: GitHub Actions executando a cada 30 minutos

## 📦 Tecnologias

- **Frontend**: Streamlit 1.28+
- **Database**: SQLite com SQLAlchemy
- **Visualização**: Plotly, Altair
- **Automação**: GitHub Actions
- **Deploy**: Streamlit Cloud

## 🛠️ Instalação Local

```bash
# 1. Clone o repositório
git clone https://github.com/Gms006/Controle-de-Processos.git
cd Controle-de-Processos

# 2. Instale as dependências
cd streamlit_app
pip install -r requirements.txt

# 3. Configure os secrets
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edite secrets.toml com suas credenciais

# 4. Execute o dashboard
streamlit run app.py
```

## ☁️ Deploy no Streamlit Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Conecte com seu GitHub
3. Selecione este repositório
4. Configure:
   - **Main file path**: `streamlit_app/app.py`
   - **Secrets**: Adicione `ACESSORIAS_API_TOKEN` e `ACESSORIAS_API_URL`
5. Clique em "Deploy"

## 🔄 Sincronização Automática

O GitHub Actions sincroniza os dados automaticamente a cada 30 minutos.

Para ativar:
1. Vá em Settings → Secrets → Actions
2. Adicione:
   - `ACESSORIAS_API_TOKEN`
   - `ACESSORIAS_API_URL`
3. Ative os workflows em Actions

## 📁 Estrutura do Projeto

```
streamlit_app/
├── app.py                    # Dashboard principal
├── pages/                    # Páginas adicionais
│   ├── 1_📋_Processos.py    # Análise de processos
│   ├── 2_🏢_Empresas.py     # Gestão de empresas
│   └── 3_⚙️_Sincronização.py # Sync management
├── components/               # Componentes reutilizáveis
│   ├── charts.py            # Gráficos Plotly
│   ├── filters.py           # Filtros interativos
│   └── metrics.py           # KPI cards
├── utils/                    # Utilitários
│   ├── database.py          # Gerenciamento SQLite
│   ├── formatters.py        # Formatação de dados
│   └── sync_manager.py      # Sincronização com API
└── requirements.txt         # Dependências Python
```

## 🔐 Segurança

- ✅ Secrets gerenciados via `.streamlit/secrets.toml` (não versionado)
- ✅ `.gitignore` configurado para proteger dados sensíveis
- ✅ Database local não versionado

## 📈 KPIs Monitorados

1. Total de Processos
2. Processos Ativos
3. Processos Concluídos
4. Taxa de Conclusão
5. Tempo Médio de Conclusão
6. Processos em Atraso
7. Empresas Ativas
8. Média de Passos por Processo

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## 📄 Licença

Este projeto é de uso interno da Acessórias Contábil.

---

**Desenvolvido com ❤️ usando Streamlit**
