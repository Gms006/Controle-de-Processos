"""
Componentes de Métricas
Cards e visualizações de KPIs
"""
import streamlit as st
from typing import Optional


def metric_card(label: str, value: str, delta: Optional[str] = None, 
                delta_color: str = "normal", help_text: str = None):
    """
    Exibe um card de métrica estilizado
    
    Args:
        label: Título da métrica
        value: Valor principal
        delta: Valor de variação (opcional)
        delta_color: 'normal', 'inverse' ou 'off'
        help_text: Texto de ajuda (tooltip)
    """
    st.metric(
        label=label,
        value=value,
        delta=delta,
        delta_color=delta_color,
        help=help_text
    )


def progress_metric(label: str, value: float, max_value: float = 100, 
                    format_str: str = "{:.1f}%"):
    """
    Exibe métrica com barra de progresso
    
    Args:
        label: Título da métrica
        value: Valor atual
        max_value: Valor máximo
        format_str: Formato de exibição do valor
    """
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.write(f"**{label}**")
        st.progress(min(value / max_value, 1.0))
    
    with col2:
        st.metric("", format_str.format(value))


def stats_grid(stats: dict, cols: int = 4):
    """
    Exibe grid de estatísticas
    
    Args:
        stats: Dicionário {label: value}
        cols: Número de colunas
    """
    columns = st.columns(cols)
    
    for idx, (label, value) in enumerate(stats.items()):
        with columns[idx % cols]:
            st.metric(label, value)


def alert_box(message: str, alert_type: str = "info"):
    """
    Exibe caixa de alerta
    
    Args:
        message: Mensagem a exibir
        alert_type: 'info', 'success', 'warning', 'error'
    """
    if alert_type == "info":
        st.info(message)
    elif alert_type == "success":
        st.success(message)
    elif alert_type == "warning":
        st.warning(message)
    elif alert_type == "error":
        st.error(message)


def kpi_row(kpis: list):
    """
    Exibe linha de KPIs
    
    Args:
        kpis: Lista de dicts com {label, value, delta (opcional)}
    """
    cols = st.columns(len(kpis))
    
    for idx, kpi in enumerate(kpis):
        with cols[idx]:
            st.metric(
                label=kpi.get('label', ''),
                value=kpi.get('value', ''),
                delta=kpi.get('delta'),
                delta_color=kpi.get('delta_color', 'normal'),
                help=kpi.get('help')
            )


def status_badge(status: str) -> str:
    """
    Retorna badge HTML para status
    
    Args:
        status: Status do processo
    
    Returns:
        String HTML com badge colorido
    """
    status_lower = status.lower() if status else ""
    
    if 'conclu' in status_lower:
        color = "#28a745"
        icon = "✅"
    elif 'andamento' in status_lower:
        color = "#ffc107"
        icon = "🔄"
    elif 'parado' in status_lower:
        color = "#dc3545"
        icon = "⏸️"
    else:
        color = "#6c757d"
        icon = "⚪"
    
    return f'<span style="background-color: {color}; color: white; padding: 4px 8px; border-radius: 4px; font-size: 0.85em;">{icon} {status}</span>'


def empty_state(message: str = "Nenhum dado encontrado", icon: str = "📭"):
    """
    Exibe estado vazio
    
    Args:
        message: Mensagem a exibir
        icon: Emoji/ícone
    """
    st.markdown(
        f"""
        <div style="text-align: center; padding: 60px 20px; color: #666;">
            <div style="font-size: 48px; margin-bottom: 16px;">{icon}</div>
            <div style="font-size: 18px;">{message}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def divider_with_text(text: str):
    """Divisor com texto no meio"""
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; margin: 20px 0;">
            <hr style="flex: 1; border: none; border-top: 1px solid #ddd;">
            <span style="padding: 0 16px; color: #666; font-weight: 500;">{text}</span>
            <hr style="flex: 1; border: none; border-top: 1px solid #ddd;">
        </div>
        """,
        unsafe_allow_html=True
    )
