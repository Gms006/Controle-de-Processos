"""
🏢 EMPRESAS - Análise por Empresa
Visualização de performance e métricas por empresa
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from utils import (
    DatabaseManager, format_percentage, format_days, 
    format_cnpj
)
from components import empty_state, bar_chart


# ============ CONFIGURAÇÃO ============
st.set_page_config(
    page_title="Empresas | Gestão Acessórias",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 Empresas - Análise de Performance")
st.markdown("---")


# ============ CARREGAR DADOS ============
@st.cache_resource
def get_db():
    return DatabaseManager()

db = get_db()


# ============ SIDEBAR - FILTROS ============
st.sidebar.header("🔍 Filtros")

busca = st.sidebar.text_input(
    "🔎 Buscar Empresa",
    placeholder="Digite o nome ou CNPJ..."
)

ordenacao = st.sidebar.selectbox(
    "📊 Ordenar por",
    options=[
        'Nome (A-Z)',
        'Total de Processos (Maior)',
        'Média de Conclusão (Maior)',
        'Média de Dias (Menor)'
    ],
    index=0
)


# ============ CARREGAR EMPRESAS ============
empresas_df = db.get_empresas()

# Aplicar busca
if busca:
    empresas_df = empresas_df[
        empresas_df['nome'].str.contains(busca, case=False, na=False) |
        empresas_df['cnpj'].str.contains(busca, case=False, na=False)
    ]

# Aplicar ordenação
if ordenacao == 'Nome (A-Z)':
    empresas_df = empresas_df.sort_values('nome')
elif ordenacao == 'Total de Processos (Maior)':
    empresas_df = empresas_df.sort_values('total_processos', ascending=False)
elif ordenacao == 'Média de Conclusão (Maior)':
    empresas_df = empresas_df.sort_values('media_conclusao', ascending=False)
elif ordenacao == 'Média de Dias (Menor)':
    empresas_df = empresas_df.sort_values('media_dias')


# ============ MÉTRICAS RESUMIDAS ============
if len(empresas_df) > 0:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🏢 Total de Empresas", len(empresas_df))
    
    with col2:
        total_processos = empresas_df['total_processos'].sum()
        st.metric("📋 Total de Processos", int(total_processos))
    
    with col3:
        media_geral = empresas_df['media_conclusao'].mean()
        st.metric("📈 Média Conclusão Geral", format_percentage(media_geral))
    
    with col4:
        media_dias_geral = empresas_df['media_dias'].mean()
        st.metric("⏱️ Tempo Médio Geral", format_days(int(media_dias_geral)))
    
    st.markdown("---")


# ============ TOP PERFORMERS ============
if len(empresas_df) > 0:
    st.markdown("## 🏆 Top 10 Empresas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ⚡ Mais Rápidas (Menor Tempo)")
        
        top_rapidas = empresas_df[empresas_df['media_dias'] > 0].nsmallest(10, 'media_dias')
        
        if len(top_rapidas) > 0:
            df_rapidas = top_rapidas[['nome', 'media_dias']].copy()
            df_rapidas['media_dias'] = df_rapidas['media_dias'].apply(lambda x: int(x))
            
            bar_chart(
                df_rapidas,
                x_col='nome',
                y_col='media_dias',
                title="",
                orientation='h',
                height=350
            )
        else:
            empty_state("Sem dados suficientes")
    
    with col2:
        st.markdown("### 🐌 Mais Lentas (Maior Tempo)")
        
        top_lentas = empresas_df[empresas_df['media_dias'] > 0].nlargest(10, 'media_dias')
        
        if len(top_lentas) > 0:
            df_lentas = top_lentas[['nome', 'media_dias']].copy()
            df_lentas['media_dias'] = df_lentas['media_dias'].apply(lambda x: int(x))
            
            bar_chart(
                df_lentas,
                x_col='nome',
                y_col='media_dias',
                title="",
                orientation='h',
                height=350
            )
        else:
            empty_state("Sem dados suficientes")
    
    st.markdown("---")


# ============ TABELA DE EMPRESAS ============
st.markdown("## 📊 Lista de Empresas")

if len(empresas_df) > 0:
    # Preparar dados para exibição
    df_display = empresas_df.copy()
    
    # Formatar colunas
    df_display['cnpj'] = df_display['cnpj'].apply(format_cnpj)
    df_display['media_conclusao'] = df_display['media_conclusao'].apply(
        lambda x: f"{x:.1f}%" if pd.notna(x) else "0%"
    )
    df_display['media_dias'] = df_display['media_dias'].apply(
        lambda x: f"{int(x)} dias" if pd.notna(x) and x > 0 else "-"
    )
    df_display['total_processos'] = df_display['total_processos'].apply(
        lambda x: int(x) if pd.notna(x) else 0
    )
    
    # Renomear colunas
    colunas_renomeadas = {
        'id': 'ID',
        'codigo': 'Código',
        'nome': 'Empresa',
        'cnpj': 'CNPJ',
        'regime_tributario': 'Regime',
        'total_processos': 'Total Processos',
        'media_conclusao': 'Média Conclusão',
        'media_dias': 'Tempo Médio'
    }
    
    df_display = df_display.rename(columns=colunas_renomeadas)
    
    # Selecionar colunas para exibir
    colunas_exibir = [
        'Código', 'Empresa', 'CNPJ', 'Regime', 
        'Total Processos', 'Média Conclusão', 'Tempo Médio'
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
    
    csv = df_display.to_csv(index=False, encoding='utf-8-sig', sep=';')
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.download_button(
            label="📥 Baixar CSV",
            data=csv,
            file_name="empresas_analise.csv",
            mime="text/csv"
        )
    
    with col2:
        st.metric("📊 Total de empresas", len(df_display))

else:
    empty_state("Nenhuma empresa encontrada")


# ============ ANÁLISE DE DISTRIBUIÇÃO ============
if len(empresas_df) > 0:
    st.markdown("---")
    st.markdown("## 📊 Distribuição por Regime Tributário")
    
    if 'regime_tributario' in empresas_df.columns:
        regime_counts = empresas_df['regime_tributario'].value_counts().reset_index()
        regime_counts.columns = ['regime', 'quantidade']
        
        if len(regime_counts) > 0:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                bar_chart(
                    regime_counts,
                    x_col='regime',
                    y_col='quantidade',
                    title="",
                    height=350
                )
            
            with col2:
                st.markdown("### 📈 Estatísticas")
                for _, row in regime_counts.iterrows():
                    pct = (row['quantidade'] / len(empresas_df) * 100)
                    st.metric(
                        row['regime'],
                        f"{int(row['quantidade'])} empresas",
                        delta=f"{pct:.1f}%"
                    )


# ============ DETALHES DA EMPRESA ============
if len(empresas_df) > 0:
    st.markdown("---")
    st.markdown("## 🔍 Detalhes por Empresa")
    
    # Seletor de empresa
    empresas_options = empresas_df.apply(
        lambda row: f"{row['codigo']} - {row['nome']}", axis=1
    ).tolist()
    
    empresa_selecionada = st.selectbox(
        "Selecione uma empresa para ver seus processos:",
        options=empresas_options,
        index=0
    )
    
    if empresa_selecionada:
        emp_codigo = empresa_selecionada.split(' - ')[0]
        
        # Buscar dados da empresa
        empresa_info = empresas_df[empresas_df['codigo'] == emp_codigo].iloc[0]
        
        # Informações da empresa
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📋 Processos", int(empresa_info['total_processos']))
        
        with col2:
            st.metric("📈 Média Conclusão", format_percentage(empresa_info['media_conclusao']))
        
        with col3:
            st.metric("⏱️ Tempo Médio", format_days(int(empresa_info['media_dias'])))
        
        with col4:
            st.metric("💼 Regime", empresa_info['regime_tributario'] or '-')
        
        st.markdown("---")
        
        # Buscar processos da empresa
        processos_empresa = db.get_processos(empresa_id=empresa_info['id'])
        
        if len(processos_empresa) > 0:
            st.markdown(f"### 📋 Processos de {empresa_info['nome']}")
            
            # Preparar dados
            df_proc = processos_empresa.copy()
            df_proc['porcentagem_conclusao'] = df_proc['porcentagem_conclusao'].apply(
                lambda x: f"{x:.1f}%" if pd.notna(x) else "0%"
            )
            
            st.dataframe(
                df_proc[['processo', 'competencia', 'status', 'porcentagem_conclusao', 'dias_corridos']],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("ℹ️ Nenhum processo encontrado para esta empresa")


# ============ FOOTER ============
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>💡 <b>Dica:</b> Use a busca para encontrar empresas específicas rapidamente</p>
    </div>
    """,
    unsafe_allow_html=True
)
