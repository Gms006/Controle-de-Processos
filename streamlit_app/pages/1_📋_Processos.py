"""
📋 PROCESSOS - Análise Detalhada
Visualização e análise completa de todos os processos
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from utils import (
    DatabaseManager, format_percentage, format_days, 
    format_date, get_status_color, format_cnpj
)
from components import search_box, empty_state, bar_chart


# ============ CONFIGURAÇÃO ============
st.set_page_config(
    page_title="Processos | Gestão Acessórias",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Processos - Análise Detalhada")
st.markdown("---")


# ============ CARREGAR DADOS ============
@st.cache_resource
def get_db():
    return DatabaseManager()

db = get_db()


# ============ SIDEBAR - FILTROS ============
st.sidebar.header("🔍 Filtros")

competencias = db.get_competencias_disponiveis()
competencia = st.sidebar.selectbox(
    "📅 Competência",
    options=['Todas'] + competencias,
    index=0
)

regimes = db.get_regimes_disponiveis()
regime = st.sidebar.selectbox(
    "💼 Regime Tributário",
    options=['Todos'] + regimes,
    index=0
)

status_options = ['Concluído', 'Em Andamento', 'Parado']
status = st.sidebar.selectbox(
    "⚡ Status",
    options=['Todos'] + status_options,
    index=0
)

# Busca
st.sidebar.markdown("---")
busca = st.sidebar.text_input(
    "🔎 Buscar Empresa",
    placeholder="Digite o nome ou CNPJ..."
)


# ============ CARREGAR PROCESSOS ============
comp_filter = None if competencia == 'Todas' else competencia
regime_filter = None if regime == 'Todos' else regime
status_filter = None if status == 'Todos' else status

processos_df = db.get_processos(
    competencia=comp_filter,
    regime=regime_filter,
    status=status_filter
)

# Aplicar busca
if busca:
    processos_df = processos_df[
        processos_df['empresa'].str.contains(busca, case=False, na=False) |
        processos_df['cnpj'].str.contains(busca, case=False, na=False)
    ]


# ============ MÉTRICAS RESUMIDAS ============
if len(processos_df) > 0:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Total", len(processos_df))
    
    with col2:
        concluidos = len(processos_df[processos_df['status'].str.contains('Conclu', case=False, na=False)])
        st.metric("✅ Concluídos", concluidos, 
                 delta=f"{(concluidos/len(processos_df)*100):.1f}%")
    
    with col3:
        media_conclusao = processos_df['porcentagem_conclusao'].mean()
        st.metric("📈 Média Conclusão", format_percentage(media_conclusao))
    
    with col4:
        media_dias = processos_df['dias_corridos'].mean()
        st.metric("⏱️ Tempo Médio", format_days(int(media_dias)))
    
    st.markdown("---")


# ============ GRÁFICO DE BARRAS - TOP EMPRESAS ============
if len(processos_df) > 0:
    st.markdown("## 📊 Top 10 Empresas - Mais Processos")
    
    top_empresas = processos_df['empresa'].value_counts().head(10).reset_index()
    top_empresas.columns = ['empresa', 'quantidade']
    
    bar_chart(
        top_empresas,
        x_col='empresa',
        y_col='quantidade',
        title="",
        height=350
    )
    
    st.markdown("---")


# ============ TABELA INTERATIVA ============
st.markdown("## 📋 Lista de Processos")

if len(processos_df) > 0:
    # Preparar dados para exibição
    df_display = processos_df.copy()
    
    # Formatar colunas
    df_display['cnpj'] = df_display['cnpj'].apply(format_cnpj)
    df_display['porcentagem_conclusao'] = df_display['porcentagem_conclusao'].apply(
        lambda x: f"{x:.1f}%" if pd.notna(x) else "0%"
    )
    df_display['data_inicio'] = df_display['data_inicio'].apply(format_date)
    df_display['data_conclusao'] = df_display['data_conclusao'].apply(format_date)
    
    # Renomear colunas
    colunas_renomeadas = {
        'proc_id': 'ID',
        'empresa': 'Empresa',
        'cnpj': 'CNPJ',
        'processo': 'Processo',
        'competencia': 'Competência',
        'status': 'Status',
        'porcentagem_conclusao': 'Progresso',
        'dias_corridos': 'Dias',
        'data_inicio': 'Início',
        'data_conclusao': 'Conclusão',
        'gestor': 'Gestor',
        'departamento': 'Departamento'
    }
    
    df_display = df_display.rename(columns=colunas_renomeadas)
    
    # Selecionar colunas para exibir
    colunas_exibir = [
        'ID', 'Empresa', 'CNPJ', 'Processo', 'Competência', 
        'Status', 'Progresso', 'Dias', 'Gestor'
    ]
    
    # Configuração da tabela
    st.dataframe(
        df_display[colunas_exibir],
        use_container_width=True,
        hide_index=True,
        height=500
    )
    
    # Botão de download
    st.markdown("---")
    
    # Preparar CSV
    csv = df_display.to_csv(index=False, encoding='utf-8-sig', sep=';')
    
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        st.download_button(
            label="📥 Baixar CSV",
            data=csv,
            file_name=f"processos_{comp_filter or 'todas'}.csv",
            mime="text/csv"
        )
    
    with col2:
        st.metric("📊 Total de registros", len(df_display))

else:
    empty_state("Nenhum processo encontrado com os filtros selecionados")


# ============ ANÁLISE DE DISTRIBUIÇÃO ============
if len(processos_df) > 0:
    st.markdown("---")
    st.markdown("## 📊 Análise de Distribuição")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribuição por Departamento
        if 'departamento' in processos_df.columns:
            dept_counts = processos_df['departamento'].value_counts().head(10).reset_index()
            dept_counts.columns = ['departamento', 'quantidade']
            
            if len(dept_counts) > 0:
                bar_chart(
                    dept_counts,
                    x_col='departamento',
                    y_col='quantidade',
                    title="📂 Por Departamento",
                    height=300
                )
    
    with col2:
        # Distribuição por Gestor
        if 'gestor' in processos_df.columns:
            gestor_counts = processos_df['gestor'].value_counts().head(10).reset_index()
            gestor_counts.columns = ['gestor', 'quantidade']
            
            if len(gestor_counts) > 0:
                bar_chart(
                    gestor_counts,
                    x_col='gestor',
                    y_col='quantidade',
                    title="👤 Por Gestor",
                    height=300
                )


# ============ DETALHES DO PROCESSO ============
if len(processos_df) > 0:
    st.markdown("---")
    st.markdown("## 🔍 Detalhes do Processo")
    
    # Seletor de processo
    processos_options = processos_df.apply(
        lambda row: f"{row['proc_id']} - {row['empresa']} - {row['processo']}", axis=1
    ).tolist()
    
    processo_selecionado = st.selectbox(
        "Selecione um processo para ver detalhes:",
        options=processos_options,
        index=0
    )
    
    if processo_selecionado:
        proc_id = int(processo_selecionado.split(' - ')[0])
        
        # Buscar passos do processo
        passos_df = db.get_passos_por_processo(proc_id)
        
        if len(passos_df) > 0:
            st.markdown(f"### 📝 Passos do Processo #{proc_id}")
            
            # Métricas dos passos
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("📊 Total de Passos", len(passos_df))
            
            with col2:
                concluidos = passos_df['concluido'].sum()
                st.metric("✅ Concluídos", concluidos)
            
            with col3:
                taxa = (concluidos / len(passos_df) * 100) if len(passos_df) > 0 else 0
                st.metric("📈 Taxa", f"{taxa:.1f}%")
            
            st.markdown("---")
            
            # Tabela de passos
            passos_display = passos_df.copy()
            passos_display['concluido'] = passos_display['concluido'].apply(
                lambda x: '✅ Sim' if x else '⏳ Não'
            )
            passos_display['data_conclusao'] = passos_display['data_conclusao'].apply(format_date)
            
            st.dataframe(
                passos_display[['ordem', 'nome', 'concluido', 'responsavel', 'data_conclusao']],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("ℹ️ Nenhum passo encontrado para este processo")


# ============ FOOTER ============
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>💡 <b>Dica:</b> Use os filtros na barra lateral para refinar sua busca</p>
    </div>
    """,
    unsafe_allow_html=True
)
