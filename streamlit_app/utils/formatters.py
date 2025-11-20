"""
Formatadores e Utilitários
Funções auxiliares para formatação de dados
"""
from datetime import datetime
from typing import Optional


def format_percentage(value: float) -> str:
    """Formata porcentagem com 1 casa decimal"""
    if value is None:
        return "0%"
    return f"{value:.1f}%"


def format_days(days: int) -> str:
    """Formata dias corridos"""
    if days is None or days == 0:
        return "-"
    if days == 1:
        return "1 dia"
    return f"{days} dias"


def format_currency(value: float) -> str:
    """Formata valor monetário em BRL"""
    if value is None:
        return "R$ 0,00"
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def format_date(date_str: Optional[str], format_out: str = "%d/%m/%Y") -> str:
    """Formata data de ISO para formato brasileiro"""
    if not date_str:
        return "-"
    
    try:
        # Tentar vários formatos de entrada
        for fmt in ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d", "%d/%m/%Y"]:
            try:
                dt = datetime.strptime(date_str[:19] if 'T' in date_str else date_str, fmt)
                return dt.strftime(format_out)
            except:
                continue
        return date_str
    except:
        return date_str


def format_datetime(date_str: Optional[str]) -> str:
    """Formata data e hora"""
    return format_date(date_str, "%d/%m/%Y %H:%M")


def format_competencia(comp: str) -> str:
    """Formata competência (YYYY-MM) para formato brasileiro"""
    if not comp or len(comp) != 7:
        return comp
    
    try:
        ano, mes = comp.split('-')
        meses = {
            '01': 'Janeiro', '02': 'Fevereiro', '03': 'Março',
            '04': 'Abril', '05': 'Maio', '06': 'Junho',
            '07': 'Julho', '08': 'Agosto', '09': 'Setembro',
            '10': 'Outubro', '11': 'Novembro', '12': 'Dezembro'
        }
        return f"{meses.get(mes, mes)}/{ano}"
    except:
        return comp


def get_status_color(status: str) -> str:
    """Retorna cor baseada no status"""
    status_lower = status.lower() if status else ""
    
    if 'conclu' in status_lower:
        return "🟢"
    elif 'andamento' in status_lower:
        return "🟡"
    elif 'parado' in status_lower or 'bloqueado' in status_lower:
        return "🔴"
    else:
        return "⚪"


def get_progress_bar(percentage: float, width: int = 20) -> str:
    """Retorna barra de progresso em texto"""
    if percentage is None:
        percentage = 0
    
    filled = int((percentage / 100) * width)
    empty = width - filled
    
    return f"{'█' * filled}{'░' * empty} {percentage:.1f}%"


def get_status_emoji(concluido: bool) -> str:
    """Retorna emoji baseado em status de conclusão"""
    return "✅" if concluido else "⏳"


def format_cnpj(cnpj: str) -> str:
    """Formata CNPJ"""
    if not cnpj:
        return "-"
    
    # Remove caracteres não numéricos
    cnpj_numbers = ''.join(filter(str.isdigit, cnpj))
    
    if len(cnpj_numbers) == 14:
        return f"{cnpj_numbers[:2]}.{cnpj_numbers[2:5]}.{cnpj_numbers[5:8]}/{cnpj_numbers[8:12]}-{cnpj_numbers[12:]}"
    
    return cnpj


def truncate_text(text: str, max_length: int = 50) -> str:
    """Trunca texto longo"""
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length - 3] + "..."


def calculate_tempo_estimado(dias_corridos: int, porcentagem: float) -> Optional[int]:
    """Calcula tempo estimado para conclusão"""
    if porcentagem is None or porcentagem == 0:
        return None
    
    if porcentagem >= 100:
        return 0
    
    # Regra de 3: se X dias = Y%, então 100% = ?
    dias_totais = (dias_corridos * 100) / porcentagem
    dias_faltantes = dias_totais - dias_corridos
    
    return int(dias_faltantes)
