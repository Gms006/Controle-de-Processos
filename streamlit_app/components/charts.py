"""
Componentes de Gráficos
Visualizações interativas com Plotly
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Optional


def pie_chart(df: pd.DataFrame, values_col: str, names_col: str, 
              title: str = "", height: int = 400):
    """
    Gráfico de pizza
    
    Args:
        df: DataFrame com dados
        values_col: Coluna de valores
        names_col: Coluna de nomes/labels
        title: Título do gráfico
        height: Altura em pixels
    """
    fig = px.pie(
        df,
        values=values_col,
        names=names_col,
        title=title,
        hole=0.4  # Donut chart
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=height, showlegend=True)
    
    st.plotly_chart(fig, use_container_width=True)


def bar_chart(df: pd.DataFrame, x_col: str, y_col: str, 
              title: str = "", orientation: str = 'v', 
              color_col: Optional[str] = None, height: int = 400):
    """
    Gráfico de barras
    
    Args:
        df: DataFrame com dados
        x_col: Coluna do eixo X
        y_col: Coluna do eixo Y
        title: Título do gráfico
        orientation: 'v' (vertical) ou 'h' (horizontal)
        color_col: Coluna para colorir barras
        height: Altura em pixels
    """
    fig = px.bar(
        df,
        x=x_col if orientation == 'v' else y_col,
        y=y_col if orientation == 'v' else x_col,
        color=color_col,
        title=title,
        orientation=orientation,
        text_auto=True
    )
    
    fig.update_layout(height=height, showlegend=bool(color_col))
    
    st.plotly_chart(fig, use_container_width=True)


def line_chart(df: pd.DataFrame, x_col: str, y_col: str, 
               title: str = "", color_col: Optional[str] = None,
               height: int = 400):
    """
    Gráfico de linha
    
    Args:
        df: DataFrame com dados
        x_col: Coluna do eixo X (geralmente datas)
        y_col: Coluna do eixo Y
        title: Título do gráfico
        color_col: Coluna para múltiplas linhas
        height: Altura em pixels
    """
    fig = px.line(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        title=title,
        markers=True
    )
    
    fig.update_layout(height=height)
    
    st.plotly_chart(fig, use_container_width=True)


def histogram(df: pd.DataFrame, column: str, title: str = "", 
              bins: int = 20, height: int = 400):
    """
    Histograma
    
    Args:
        df: DataFrame com dados
        column: Coluna para histograma
        title: Título do gráfico
        bins: Número de bins
        height: Altura em pixels
    """
    fig = px.histogram(
        df,
        x=column,
        title=title,
        nbins=bins
    )
    
    fig.update_layout(height=height)
    
    st.plotly_chart(fig, use_container_width=True)


def gauge_chart(value: float, title: str = "", max_value: float = 100,
                thresholds: dict = None, height: int = 300):
    """
    Gráfico de gauge (velocímetro)
    
    Args:
        value: Valor atual
        title: Título do gráfico
        max_value: Valor máximo
        thresholds: Dict com {limite: cor} ex: {30: 'red', 70: 'yellow', 100: 'green'}
        height: Altura em pixels
    """
    if thresholds is None:
        thresholds = {30: 'red', 70: 'yellow', 100: 'green'}
    
    # Determinar cor baseada nos thresholds
    color = 'gray'
    for threshold, threshold_color in sorted(thresholds.items()):
        if value <= threshold:
            color = threshold_color
            break
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        gauge={
            'axis': {'range': [None, max_value]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 30], 'color': "lightgray"},
                {'range': [30, 70], 'color': "gray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': max_value * 0.9
            }
        }
    ))
    
    fig.update_layout(height=height)
    
    st.plotly_chart(fig, use_container_width=True)


def timeline_chart(df: pd.DataFrame, start_col: str, end_col: str,
                   name_col: str, title: str = "", height: int = 400):
    """
    Gráfico de timeline (Gantt)
    
    Args:
        df: DataFrame com dados
        start_col: Coluna de data início
        end_col: Coluna de data fim
        name_col: Coluna com nome da tarefa
        title: Título do gráfico
        height: Altura em pixels
    """
    fig = px.timeline(
        df,
        x_start=start_col,
        x_end=end_col,
        y=name_col,
        title=title
    )
    
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(height=height)
    
    st.plotly_chart(fig, use_container_width=True)


def scatter_plot(df: pd.DataFrame, x_col: str, y_col: str,
                 title: str = "", color_col: Optional[str] = None,
                 size_col: Optional[str] = None, height: int = 400):
    """
    Gráfico de dispersão
    
    Args:
        df: DataFrame com dados
        x_col: Coluna do eixo X
        y_col: Coluna do eixo Y
        title: Título do gráfico
        color_col: Coluna para colorir pontos
        size_col: Coluna para tamanho dos pontos
        height: Altura em pixels
    """
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        size=size_col,
        title=title,
        hover_data=df.columns
    )
    
    fig.update_layout(height=height)
    
    st.plotly_chart(fig, use_container_width=True)


def heatmap(df: pd.DataFrame, x_col: str, y_col: str, value_col: str,
            title: str = "", height: int = 400):
    """
    Mapa de calor
    
    Args:
        df: DataFrame com dados
        x_col: Coluna do eixo X
        y_col: Coluna do eixo Y
        value_col: Coluna de valores
        title: Título do gráfico
        height: Altura em pixels
    """
    pivot_df = df.pivot(index=y_col, columns=x_col, values=value_col)
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_df.values,
        x=pivot_df.columns,
        y=pivot_df.index,
        colorscale='RdYlGn'
    ))
    
    fig.update_layout(title=title, height=height)
    
    st.plotly_chart(fig, use_container_width=True)
