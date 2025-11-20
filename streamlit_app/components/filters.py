"""
Componentes de Filtros
Filtros interativos para dashboards
"""
import streamlit as st
import pandas as pd
from typing import List, Optional, Any
from datetime import datetime, timedelta


def filter_sidebar(
    competencias: List[str] = None,
    regimes: List[str] = None,
    status_options: List[str] = None
) -> dict:
    """
    Cria sidebar com filtros padrão
    
    Args:
        competencias: Lista de competências disponíveis
        regimes: Lista de regimes tributários
        status_options: Lista de status possíveis
    
    Returns:
        Dict com filtros selecionados
    """
    st.sidebar.header("🔍 Filtros")
    
    filtros = {}
    
    # Filtro de Competência
    if competencias:
        filtros['competencia'] = st.sidebar.selectbox(
            "📅 Competência",
            options=['Todas'] + competencias,
            index=0
        )
    
    # Filtro de Regime Tributário
    if regimes:
        filtros['regime'] = st.sidebar.selectbox(
            "📊 Regime Tributário",
            options=['Todos'] + regimes,
            index=0
        )
    
    # Filtro de Status
    if status_options:
        filtros['status'] = st.sidebar.multiselect(
            "⚡ Status",
            options=status_options,
            default=status_options
        )
    
    # Filtro de Data
    st.sidebar.markdown("---")
    filtros['periodo'] = st.sidebar.date_input(
        "📆 Período",
        value=(
            datetime.now() - timedelta(days=30),
            datetime.now()
        ),
        help="Filtrar por período de início do processo"
    )
    
    return filtros


def search_box(placeholder: str = "Buscar...", key: str = "search") -> str:
    """
    Caixa de busca
    
    Args:
        placeholder: Texto placeholder
        key: Chave única do widget
    
    Returns:
        Texto digitado
    """
    return st.text_input(
        "🔎 Buscar",
        placeholder=placeholder,
        key=key
    )


def multiselect_filter(
    label: str,
    options: List[Any],
    default: Optional[List[Any]] = None,
    key: str = None
) -> List[Any]:
    """
    Filtro de múltipla seleção
    
    Args:
        label: Label do filtro
        options: Lista de opções
        default: Opções pré-selecionadas
        key: Chave única do widget
    
    Returns:
        Lista de itens selecionados
    """
    if default is None:
        default = options
    
    return st.multiselect(
        label,
        options=options,
        default=default,
        key=key
    )


def slider_filter(
    label: str,
    min_value: float,
    max_value: float,
    default: tuple = None,
    key: str = None
) -> tuple:
    """
    Filtro de slider (range)
    
    Args:
        label: Label do filtro
        min_value: Valor mínimo
        max_value: Valor máximo
        default: Tupla (min, max) pré-selecionada
        key: Chave única do widget
    
    Returns:
        Tupla (min, max) selecionada
    """
    if default is None:
        default = (min_value, max_value)
    
    return st.slider(
        label,
        min_value=min_value,
        max_value=max_value,
        value=default,
        key=key
    )


def quick_filters(options: List[str], key: str = "quick_filter") -> str:
    """
    Filtros rápidos em pills/botões
    
    Args:
        options: Lista de opções
        key: Chave única
    
    Returns:
        Opção selecionada
    """
    cols = st.columns(len(options))
    
    selected = None
    for idx, option in enumerate(options):
        with cols[idx]:
            if st.button(option, key=f"{key}_{idx}"):
                selected = option
    
    return selected


def date_range_filter(
    label: str = "Período",
    key: str = "date_range"
) -> tuple:
    """
    Filtro de range de datas
    
    Args:
        label: Label do filtro
        key: Chave única
    
    Returns:
        Tupla (data_inicio, data_fim)
    """
    col1, col2 = st.columns(2)
    
    with col1:
        data_inicio = st.date_input(
            f"{label} - Início",
            value=datetime.now() - timedelta(days=30),
            key=f"{key}_inicio"
        )
    
    with col2:
        data_fim = st.date_input(
            f"{label} - Fim",
            value=datetime.now(),
            key=f"{key}_fim"
        )
    
    return (data_inicio, data_fim)


def apply_filters_to_dataframe(
    df: pd.DataFrame,
    filtros: dict
) -> pd.DataFrame:
    """
    Aplica filtros a um DataFrame
    
    Args:
        df: DataFrame original
        filtros: Dict com filtros {coluna: valor}
    
    Returns:
        DataFrame filtrado
    """
    df_filtered = df.copy()
    
    for coluna, valor in filtros.items():
        if valor is None or valor == 'Todos' or valor == 'Todas':
            continue
        
        if isinstance(valor, list):
            # Filtro de múltipla seleção
            if len(valor) > 0:
                df_filtered = df_filtered[df_filtered[coluna].isin(valor)]
        
        elif isinstance(valor, tuple):
            # Filtro de range
            if len(valor) == 2:
                df_filtered = df_filtered[
                    (df_filtered[coluna] >= valor[0]) &
                    (df_filtered[coluna] <= valor[1])
                ]
        
        else:
            # Filtro simples
            df_filtered = df_filtered[df_filtered[coluna] == valor]
    
    return df_filtered
