"""
Utilitários - Funções auxiliares
"""

import json
import logging
from datetime import datetime
from pathlib import Path


def carregar_config(arquivo: str = "config/config.json") -> dict:
    """Carrega arquivo de configuração"""
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            config = json.load(f)
        logging.info(f"✓ Configuração carregada: {arquivo}")
        return config
    except FileNotFoundError:
        logging.error(f"❌ Arquivo de configuração não encontrado: {arquivo}")
        return {}
    except json.JSONDecodeError as e:
        logging.error(f"❌ Erro ao decodificar JSON: {e}")
        return {}


def salvar_json(dados: dict, arquivo: str):
    """Salva dados em formato JSON"""
    try:
        filepath = Path(arquivo)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        
        logging.info(f"✓ Dados salvos: {arquivo}")
        return True
    except Exception as e:
        logging.error(f"❌ Erro ao salvar JSON: {e}")
        return False


def carregar_json(arquivo: str) -> dict:
    """Carrega dados de arquivo JSON"""
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        logging.info(f"✓ Dados carregados: {arquivo}")
        return dados
    except FileNotFoundError:
        logging.error(f"❌ Arquivo não encontrado: {arquivo}")
        return {}
    except json.JSONDecodeError as e:
        logging.error(f"❌ Erro ao decodificar JSON: {e}")
        return {}


def formatar_data_br(data_iso: str) -> str:
    """Converte data ISO para formato brasileiro"""
    if not data_iso or data_iso == '0000-00-00':
        return ''
    
    try:
        # Se está em formato ISO (YYYY-MM-DD)
        if '-' in data_iso:
            partes = data_iso.split('-')
            if len(partes) == 3:
                return f"{partes[2]}/{partes[1]}/{partes[0]}"
        
        # Se já está em formato BR
        if '/' in data_iso:
            return data_iso
        
        return data_iso
    except Exception:
        return data_iso


def formatar_data_iso(data_br: str) -> str:
    """Converte data brasileira para formato ISO"""
    if not data_br or data_br == '0000-00-00':
        return ''
    
    try:
        # Se está em formato BR (DD/MM/YYYY)
        if '/' in data_br:
            partes = data_br.split('/')
            if len(partes) == 3:
                return f"{partes[2]}-{partes[1]}-{partes[0]}"
        
        # Se já está em formato ISO
        if '-' in data_br:
            return data_br
        
        return data_br
    except Exception:
        return data_br


def calcular_dias_uteis(data_inicio: str, data_fim: str) -> int:
    """
    Calcula dias úteis entre duas datas
    (Implementação simplificada - conta dias corridos por ora)
    """
    try:
        # Converter para datetime
        if '/' in data_inicio:
            data_inicio = formatar_data_iso(data_inicio)
        if '/' in data_fim:
            data_fim = formatar_data_iso(data_fim)
        
        dt_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
        dt_fim = datetime.strptime(data_fim, '%Y-%m-%d')
        
        # Calcular diferença em dias
        diff = (dt_fim - dt_inicio).days
        
        # TODO: Implementar cálculo real de dias úteis (descontando finais de semana e feriados)
        return diff
    except Exception:
        return 0


def formatar_cnpj(cnpj: str) -> str:
    """Formata CNPJ no padrão XX.XXX.XXX/XXXX-XX"""
    if not cnpj:
        return ''
    
    # Remove caracteres não numéricos
    cnpj_num = ''.join(filter(str.isdigit, cnpj))
    
    # Se já tem 14 dígitos, formata
    if len(cnpj_num) == 14:
        return f"{cnpj_num[:2]}.{cnpj_num[2:5]}.{cnpj_num[5:8]}/{cnpj_num[8:12]}-{cnpj_num[12:]}"
    
    # Se tem 11 dígitos, é CPF
    if len(cnpj_num) == 11:
        return f"{cnpj_num[:3]}.{cnpj_num[3:6]}.{cnpj_num[6:9]}-{cnpj_num[9:]}"
    
    return cnpj


def criar_diretorio(caminho: str):
    """Cria diretório se não existir"""
    try:
        Path(caminho).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logging.error(f"❌ Erro ao criar diretório {caminho}: {e}")
        return False
