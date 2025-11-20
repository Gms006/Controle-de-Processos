# 🎨 GUIA DE CUSTOMIZAÇÃO

## 💡 Como Personalizar Seu Dashboard

### **🎨 Alterar Cores do Tema**

Edite: `.streamlit/config.toml`

```toml
[theme]
primaryColor = "#1f77b4"        # Cor principal (azul) - mude aqui!
backgroundColor = "#ffffff"      # Fundo branco
secondaryBackgroundColor = "#f0f2f6"  # Fundo dos cards
textColor = "#262730"           # Cor do texto
```

**Exemplos de paletas:**
- Verde corporativo: `#28a745`
- Laranja vibrante: `#fd7e14`
- Roxo moderno: `#6f42c1`
- Azul escuro: `#0d47a1`

### **📊 Adicionar Novos Gráficos**

No arquivo `streamlit_app/components/charts.py`, você tem 8 tipos prontos:
- `pie_chart()` - Pizza/Donut
- `bar_chart()` - Barras
- `line_chart()` - Linha
- `histogram()` - Histograma
- `gauge_chart()` - Velocímetro
- `timeline_chart()` - Gantt
- `scatter_plot()` - Dispersão
- `heatmap()` - Mapa de calor

**Para usar em qualquer página:**
```python
from components import bar_chart

bar_chart(
    df=seu_dataframe,
    x_col='coluna_x',
    y_col='coluna_y',
    title="Meu Gráfico"
)
```

### **➕ Adicionar Nova Página**

1. Crie arquivo: `streamlit_app/pages/4_🎯_NovoNome.py`

2. Template básico:
```python
import streamlit as st
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from utils import DatabaseManager

st.set_page_config(
    page_title="Novo | Gestão",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Minha Nova Página")

# Seu código aqui...
```

3. Pronto! Aparecerá automaticamente no menu

### **📊 Adicionar Novo KPI no Home**

Edite: `streamlit_app/app.py`

Encontre a seção `kpis = [...]` e adicione:

```python
{
    'label': '🎯 Meu KPI',
    'value': f"{valor}",
    'delta': f"+10%",
    'help': 'Descrição do KPI'
}
```

### **🔍 Adicionar Novo Filtro**

No arquivo da página, adicione na sidebar:

```python
meu_filtro = st.sidebar.selectbox(
    "🔍 Meu Filtro",
    options=['Todos', 'Opção 1', 'Opção 2'],
    index=0
)
```

### **📥 Mudar Formato de Export**

Atualmente: CSV com separador `;`

Para mudar:
```python
# Excel em vez de CSV
df.to_excel('arquivo.xlsx', index=False)

# CSV com vírgula
df.to_csv('arquivo.csv', sep=',', index=False)

# JSON
df.to_json('arquivo.json', orient='records')
```

### **⏱️ Ajustar Tempo de Cache**

Edite os decoradores `@st.cache_data(ttl=300)`:

```python
@st.cache_data(ttl=600)  # 10 minutos
@st.cache_data(ttl=1800)  # 30 minutos
@st.cache_data(ttl=3600)  # 1 hora
```

### **🔄 Mudar Frequência da Sincronização Automática**

Edite: `.github/workflows/sync-data.yml`

```yaml
schedule:
  # A cada 3 horas: '0 */3 * * *'
  # A cada 12 horas: '0 */12 * * *'
  # Todo dia às 8h: '0 8 * * *'
  # Todo dia às 8h e 20h: '0 8,20 * * *'
  - cron: '0 */6 * * *'  # A cada 6 horas (atual)
```

### **📊 Adicionar Nova Consulta ao Banco**

Edite: `streamlit_app/utils/database.py`

Adicione método na classe `DatabaseManager`:

```python
@st.cache_data(ttl=300)
def get_minha_consulta(_self) -> pd.DataFrame:
    """Minha nova consulta customizada"""
    with sqlite3.connect(_self.db_path) as conn:
        query = """
            SELECT 
                coluna1,
                coluna2,
                COUNT(*) as total
            FROM tabela
            GROUP BY coluna1, coluna2
            ORDER BY total DESC
        """
        return pd.read_sql_query(query, conn)
```

Use na página:
```python
db = get_db()
dados = db.get_minha_consulta()
```

### **🎨 Customizar Cards de Métricas**

CSS customizado no `app.py`:

```python
st.markdown("""
    <style>
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)
```

### **📱 Adicionar Logo da Empresa**

No `app.py`, após o título:

```python
col1, col2 = st.columns([1, 4])
with col1:
    st.image("caminho/logo.png", width=100)
with col2:
    st.title("Dashboard")
```

### **🔔 Adicionar Notificações**

Para alertas mais chamativos:

```python
# Balões de comemoração
st.balloons()

# Neve (decoração)
st.snow()

# Toast notification (Streamlit 1.31+)
st.toast("✅ Dados atualizados!", icon="✅")
```

### **📊 Gráfico com Mais Detalhes**

Personalizar Plotly:

```python
import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Bar(
    x=df['categoria'],
    y=df['valor'],
    marker=dict(
        color=df['valor'],
        colorscale='Viridis',
        showscale=True
    ),
    text=df['valor'],
    textposition='auto'
))

fig.update_layout(
    title="Meu Gráfico Personalizado",
    xaxis_title="Categorias",
    yaxis_title="Valores",
    hovermode='x unified',
    plot_bgcolor='rgba(0,0,0,0)'
)

st.plotly_chart(fig, use_container_width=True)
```

### **🔐 Adicionar Autenticação (Básica)**

No início do `app.py`:

```python
def check_password():
    """Retorna True se usuário digitou senha correta"""
    def password_entered():
        if st.session_state["password"] == st.secrets["auth"]["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input(
            "Senha:", 
            type="password", 
            on_change=password_entered, 
            key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        st.text_input(
            "Senha:", 
            type="password", 
            on_change=password_entered, 
            key="password"
        )
        st.error("❌ Senha incorreta")
        return False
    else:
        return True

if not check_password():
    st.stop()

# Resto do código...
```

Adicionar no `secrets.toml`:
```toml
[auth]
password = "sua_senha_aqui"
```

### **📧 Enviar Email com Relatório**

Instalar: `pip install sendgrid`

```python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def enviar_relatorio(destinatario, dados):
    message = Mail(
        from_email='seu@email.com',
        to_emails=destinatario,
        subject='Relatório de Processos',
        html_content=f'<h1>Relatório</h1><p>{dados}</p>'
    )
    
    sg = SendGridAPIClient(st.secrets["sendgrid"]["api_key"])
    response = sg.send(message)
```

### **⚡ Melhorar Performance**

1. **Limitar dados carregados:**
```python
# Em vez de carregar tudo:
df = db.get_processos()

# Carregue apenas o necessário:
df = db.get_processos().head(1000)  # Primeiros 1000
```

2. **Paginar tabelas grandes:**
```python
page_size = 50
page = st.number_input('Página', min_value=1, value=1)
start = (page - 1) * page_size
end = start + page_size

st.dataframe(df.iloc[start:end])
```

3. **Lazy loading:**
```python
with st.spinner("Carregando dados..."):
    dados = funcao_pesada()
```

---

## 🎯 Exemplos Prontos para Copiar

### **Adicionar Página de Análise de Tendências:**

```python
# streamlit_app/pages/4_📈_Tendências.py
import streamlit as st
import pandas as pd
from components import line_chart

st.title("📈 Análise de Tendências")

# Agrupar por mês
tendencias = processos_df.groupby(
    pd.to_datetime(processos_df['data_inicio']).dt.to_period('M')
).size().reset_index(name='quantidade')

line_chart(
    tendencias,
    x_col='data_inicio',
    y_col='quantidade',
    title="Processos Iniciados por Mês"
)
```

### **Dashboard de Gestor Individual:**

```python
gestor_selecionado = st.selectbox("Gestor:", gestores_list)

processos_gestor = processos_df[
    processos_df['gestor'] == gestor_selecionado
]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total", len(processos_gestor))
with col2:
    concluidos = len(processos_gestor[processos_gestor['status']=='Concluído'])
    st.metric("Concluídos", concluidos)
with col3:
    taxa = (concluidos / len(processos_gestor) * 100) if len(processos_gestor) > 0 else 0
    st.metric("Taxa", f"{taxa:.1f}%")
```

---

## 💡 Dicas Finais

1. **Sempre teste localmente** antes de fazer commit
2. **Use `st.write()` para debug** rápido
3. **Documente mudanças** no README
4. **Mantenha backup** do banco de dados
5. **Versione mudanças** com Git

---

**Precisa de mais ideias?** Consulte:
- https://streamlit.io/gallery
- https://plotly.com/python/
- https://docs.streamlit.io/library/api-reference

**Boa customização!** 🚀
