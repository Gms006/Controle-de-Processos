"""
🏠 DASHBOARD - GESTÃO DE PROCESSOS CONTÁBEIS
Sistema de acompanhamento de processos Acessórias

Autor: Sistema de Gestão
Data: Novembro 2025
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Adicionar diretórios ao path
sys.path.append(str(Path(__file__).parent))

from utils import DatabaseManager, format_percentage, format_days, get_status_color
from components import kpi_row, pie_chart, bar_chart, alert_box, empty_state


# ============ CONFIGURAÇÃO DA PÁGINA ============
st.set_page_config(
    page_title="Gestão de Processos | Acessórias",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ CSS CUSTOMIZADO ============
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
    }
    .stMetric label {
        font-size: 14px !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        font-size: 28px !important;
    }
    h1 {
        color: #1f77b4;
        padding-bottom: 20px;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .danger-box {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)


# ============ INICIALIZAÇÃO ============
@st.cache_resource
def get_db():
    """Inicializa conexão com banco de dados"""
    return DatabaseManager()


# ============ HEADER ============
st.title("📊 Dashboard - Gestão de Processos Contábeis")
st.markdown("**Sistema de acompanhamento de processos Acessórias**")
st.markdown("---")


# ============ CARREGAR DADOS ============
db = get_db()

# Verificar se há dados
try:
    metricas = db.get_metricas_gerais()
    
    if metricas['total_processos'] == 0:
        st.warning("⚠️ Nenhum dado encontrado no banco de dados.")
        st.info("💡 **Como adicionar dados:**\n\n"
                "1. Configure suas credenciais em `.streamlit/secrets.toml`\n"
                "2. Execute a sincronização na página **⚙️ Sincronização**\n"
                "3. Os dados serão importados da API Acessórias")
        st.stop()

except Exception as e:
    st.error(f"❌ Erro ao conectar ao banco de dados: {e}")
    st.info("Execute a sincronização inicial na página **⚙️ Sincronização**")
    st.stop()


# ============ SIDEBAR - FILTROS ============
st.sidebar.header("🔍 Filtros")

competencias = db.get_competencias_disponiveis()
competencia_selecionada = st.sidebar.selectbox(
    "📅 Competência",
    options=['Todas'] + competencias,
    index=0
)

regimes = db.get_regimes_disponiveis()
regime_selecionado = st.sidebar.selectbox(
    "📊 Regime Tributário",
    options=['Todos'] + regimes,
    index=0
)

# Aplicar filtros
competencia_filter = None if competencia_selecionada == 'Todas' else competencia_selecionada
regime_filter = None if regime_selecionado == 'Todos' else regime_selecionado

metricas = db.get_metricas_gerais(competencia=competencia_filter)
processos_df = db.get_processos(competencia=competencia_filter, regime=regime_filter)


# ============ ÚLTIMA ATUALIZAÇÃO ============
ultima_sync = db.get_ultima_sincronizacao()
if ultima_sync:
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔄 Última Atualização")
    st.sidebar.info(
        f"**Data:** {ultima_sync['concluida_em'][:19]}\n\n"
        f"**Processos:** {ultima_sync['total_processos']}\n\n"
        f"**Tempo:** {ultima_sync['tempo_execucao']}s"
    )


# ============ KPIs PRINCIPAIS ============
st.markdown("## 📈 Visão Geral")

kpis = [
    {
        'label': '📋 Total de Processos',
        'value': f"{int(metricas['total_processos']):,}".replace(',', '.'),
        'help': 'Total de processos no sistema'
    },
    {
        'label': '🏢 Empresas',
        'value': f"{int(metricas['total_empresas']):,}".replace(',', '.'),
        'help': 'Empresas com processos ativos'
    },
    {
        'label': '✅ Concluídos',
        'value': f"{int(metricas['concluidos']):,}".replace(',', '.'),
        'delta': f"{(metricas['concluidos']/metricas['total_processos']*100):.1f}%",
        'help': 'Processos finalizados'
    },
    {
        'label': '🔄 Em Andamento',
        'value': f"{int(metricas['em_andamento']):,}".replace(',', '.'),
        'delta': f"{(metricas['em_andamento']/metricas['total_processos']*100):.1f}%",
        'help': 'Processos em execução'
    }
]

kpi_row(kpis)

st.markdown("---")


# ============ SEGUNDA LINHA DE MÉTRICAS ============
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📊 Taxa de Conclusão Média",
        format_percentage(metricas['media_conclusao']),
        help="Média de progresso de todos os processos"
    )

with col2:
    st.metric(
        "⏱️ Tempo Médio",
        format_days(int(metricas['media_dias']) if metricas['media_dias'] else 0),
        help="Tempo médio de execução dos processos"
    )

with col3:
    st.metric(
        "🔴 Processos Parados",
        f"{int(metricas['parados']):,}".replace(',', '.'),
        delta=f"-{(metricas['parados']/metricas['total_processos']*100):.1f}%" if metricas['parados'] > 0 else "0%",
        delta_color="inverse",
        help="Processos com 0% de progresso"
    )

with col4:
    taxa_sucesso = (metricas['concluidos'] / metricas['total_processos'] * 100) if metricas['total_processos'] > 0 else 0
    st.metric(
        "🎯 Taxa de Sucesso",
        f"{taxa_sucesso:.1f}%",
        help="Percentual de processos concluídos"
    )

st.markdown("---")


# ============ ALERTAS CRÍTICOS ============
if metricas['parados'] > 0:
    alert_box(
        f"⚠️ **ATENÇÃO:** {int(metricas['parados'])} processos estão parados (0% de progresso). "
        f"Acesse a página **Processos** para mais detalhes.",
        alert_type="warning"
    )


# ============ GRÁFICOS ============
st.markdown("## 📊 Análises Visuais")

col1, col2 = st.columns(2)

with col1:
    # Gráfico de Status
    if len(processos_df) > 0:
        status_counts = processos_df['status'].value_counts().reset_index()
        status_counts.columns = ['status', 'quantidade']
        
        pie_chart(
            status_counts,
            values_col='quantidade',
            names_col='status',
            title="📈 Distribuição por Status",
            height=350
        )
    else:
        empty_state("Nenhum dado disponível")

with col2:
    # Gráfico de Regime Tributário
    if len(processos_df) > 0 and 'regime_tributario' in processos_df.columns:
        regime_counts = processos_df['regime_tributario'].value_counts().reset_index()
        regime_counts.columns = ['regime', 'quantidade']
        
        pie_chart(
            regime_counts,
            values_col='quantidade',
            names_col='regime',
            title="💼 Distribuição por Regime",
            height=350
        )
    else:
        empty_state("Nenhum dado disponível")


# ============ TABELA DE PROCESSOS RECENTES ============
st.markdown("---")
st.markdown("## 📋 Processos Recentes")

if len(processos_df) > 0:
    # Preparar dados para exibição
    df_display = processos_df.head(10).copy()
    
    # Formatar colunas
    df_display['porcentagem_conclusao'] = df_display['porcentagem_conclusao'].apply(
        lambda x: format_percentage(x)
    )
    df_display['dias_corridos'] = df_display['dias_corridos'].apply(
        lambda x: format_days(int(x) if pd.notna(x) else 0)
    )
    
    # Selecionar colunas para exibir
    colunas_exibir = [
        'empresa', 'processo', 'competencia', 'status', 
        'porcentagem_conclusao', 'dias_corridos'
    ]
    
    st.dataframe(
        df_display[colunas_exibir],
        use_container_width=True,
        hide_index=True
    )
    
    st.info(f"Mostrando 10 de {len(processos_df)} processos. "
            f"Acesse a página **📋 Processos** para ver todos.")
else:
    empty_state("Nenhum processo encontrado")


# ============ GRÁFICO DE PROGRESSO ============
st.markdown("---")
st.markdown("## 📈 Análise de Progresso")

if len(processos_df) > 0:
    # Criar faixas de progresso
    def get_faixa_progresso(pct):
        if pd.isna(pct):
            return 'Sem dados'
        if pct == 0:
            return '0% - Parado'
        elif pct < 25:
            return '1-24% - Inicial'
        elif pct < 50:
            return '25-49% - Em progresso'
        elif pct < 75:
            return '50-74% - Avançado'
        elif pct < 100:
            return '75-99% - Quase concluído'
        else:
            return '100% - Concluído'
    
    processos_df['faixa_progresso'] = processos_df['porcentagem_conclusao'].apply(get_faixa_progresso)
    
    faixas_counts = processos_df['faixa_progresso'].value_counts().reset_index()
    faixas_counts.columns = ['faixa', 'quantidade']
    
    # Ordenar faixas
    ordem_faixas = [
        '0% - Parado',
        '1-24% - Inicial',
        '25-49% - Em progresso',
        '50-74% - Avançado',
        '75-99% - Quase concluído',
        '100% - Concluído',
        'Sem dados'
    ]
    
    faixas_counts['faixa'] = pd.Categorical(
        faixas_counts['faixa'],
        categories=ordem_faixas,
        ordered=True
    )
    faixas_counts = faixas_counts.sort_values('faixa')
    
    bar_chart(
        faixas_counts,
        x_col='faixa',
        y_col='quantidade',
        title="📊 Distribuição por Faixa de Progresso",
        height=400
    )
else:
    empty_state("Nenhum dado disponível")


# ============ FOOTER ============
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>📊 <b>Dashboard de Gestão de Processos Contábeis</b></p>
        <p>Sistema integrado com API Acessórias | Novembro 2025</p>
    </div>
    """,
    unsafe_allow_html=True
)
