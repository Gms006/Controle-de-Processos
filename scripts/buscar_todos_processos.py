#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para buscar TODOS os tipos de processos fiscais da API Acessórias
Gera uma planilha Excel separada para cada tipo de processo

Tipos de processos:
1. Simples Nacional — Mensal
2. Lucro Presumido - Serviços
3. Lucro Presumido - Comércio, Industria e Serviços
4. Lucro Real - Comércio e Industria
5. Lucro Real - Serviços
"""

import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
from dotenv import load_dotenv

# Adicionar diretório scripts ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api_client import AcessoriasAPI
from processador_processos import ProcessadorProcessos
from exportador_excel_v2 import ExportadorExcelV2
from utils import salvar_json

# Configurar logging
def configurar_logging():
    """Configura sistema de logging"""
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f'buscar_todos_processos_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

# Definir tipos de processos
TIPOS_PROCESSOS = [
    {
        'nome': 'Simples Nacional — Mensal',
        'arquivo_prefixo': 'SimplesNacional',
        'descricao': 'Processos de empresas do Simples Nacional'
    },
    {
        'nome': 'Lucro Presumido - Serviços',
        'arquivo_prefixo': 'LucroPresumido_Servicos',
        'descricao': 'Processos de empresas do Lucro Presumido (Serviços)'
    },
    {
        'nome': 'Lucro Presumido - Comércio, Industria e Serviços',
        'arquivo_prefixo': 'LucroPresumido_Comercio',
        'descricao': 'Processos de empresas do Lucro Presumido (Comércio/Indústria)'
    },
    {
        'nome': 'Lucro Real - Comércio e Industria',
        'arquivo_prefixo': 'LucroReal_Comercio',
        'descricao': 'Processos de empresas do Lucro Real (Comércio/Indústria)'
    },
    {
        'nome': 'Lucro Real - Serviços',
        'arquivo_prefixo': 'LucroReal_Servicos',
        'descricao': 'Processos de empresas do Lucro Real (Serviços)'
    }
]

def buscar_processos_por_tipo(api: AcessoriasAPI, tipo_processo: Dict, logger) -> Tuple[List[Dict], Dict]:
    """Busca processos de um tipo específico"""
    nome = tipo_processo['nome']
    
    logger.info(f"\n{'='*70}")
    logger.info(f"BUSCANDO: {nome}")
    logger.info(f"{'='*70}")
    
    # Buscar processos em andamento
    logger.info(f"\n🔍 Buscando processos EM ANDAMENTO...")
    processos_andamento = api.get_all_processes_paginated(
        proc_status='A',
        proc_nome=nome,
        with_details=True
    )
    logger.info(f"✓ {len(processos_andamento)} processos em andamento encontrados")
    
    # Buscar processos concluídos
    logger.info(f"\n🔍 Buscando processos CONCLUÍDOS...")
    processos_concluidos = api.get_all_processes_paginated(
        proc_status='C',
        proc_nome=nome,
        with_details=True
    )
    logger.info(f"✓ {len(processos_concluidos)} processos concluídos encontrados")
    
    # Combinar todos
    todos_processos = processos_andamento + processos_concluidos
    
    # Estatísticas
    stats = {
        'total': len(todos_processos),
        'andamento': len(processos_andamento),
        'concluidos': len(processos_concluidos),
        'taxa_conclusao': (len(processos_concluidos) / len(todos_processos) * 100) if todos_processos else 0
    }
    
    logger.info(f"\n📊 RESUMO - {nome}:")
    logger.info(f"   Total: {stats['total']}")
    logger.info(f"   Em andamento: {stats['andamento']}")
    logger.info(f"   Concluídos: {stats['concluidos']}")
    logger.info(f"   Taxa de conclusão: {stats['taxa_conclusao']:.1f}%")
    
    return todos_processos, stats

def processar_e_exportar(processos: List[Dict], tipo_processo: Dict, stats: Dict, logger) -> str:
    """Processa dados e exporta para Excel"""
    if not processos:
        logger.warning(f"⚠️ Nenhum processo encontrado para {tipo_processo['nome']}. Pulando...")
        return None
    
    logger.info(f"\n📊 Processando dados de {tipo_processo['nome']}...")
    
    # Processar dados
    processador = ProcessadorProcessos()
    df_geral, df_passos, df_desdobramentos = processador.processar_lista_processos(processos)
    
    logger.info(f"   - Processos Geral: {len(df_geral)} linhas")
    logger.info(f"   - Passos: {len(df_passos)} linhas")
    logger.info(f"   - Desdobramentos: {len(df_desdobramentos)} linhas")
    
    # Exportar para Excel
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    nome_arquivo = f"{tipo_processo['arquivo_prefixo']}_DadosBrutos_{timestamp}.xlsx"
    
    logger.info(f"\n📁 Gerando planilha: output/planilhas/{nome_arquivo}")
    
    exportador = ExportadorExcelV2()
    caminho_completo = exportador.exportar_dados_brutos(
        df_geral=df_geral,
        df_passos=df_passos,
        df_desdobramentos=df_desdobramentos,
        nome_arquivo=nome_arquivo
    )
    
    logger.info(f"✓ Planilha gerada com sucesso!")
    
    # Salvar JSON backup
    json_dir = Path('data/raw')
    json_file = json_dir / f"{tipo_processo['arquivo_prefixo']}_{timestamp}.json"
    salvar_json(processos, str(json_file))
    logger.info(f"✓ Backup JSON salvo: {json_file}")
    
    return caminho_completo

def main():
    """Função principal"""
    logger = configurar_logging()
    
    logger.info("="*70)
    logger.info("INICIANDO BUSCA DE TODOS OS PROCESSOS FISCAIS")
    logger.info("="*70)
    
    # Carregar variáveis de ambiente
    load_dotenv()
    api_token = os.getenv('API_TOKEN') or os.getenv('ACESSORIAS_API_TOKEN')
    
    if not api_token:
        logger.error("❌ ERRO: Token da API não encontrado no arquivo .env")
        logger.error("Crie um arquivo .env com: API_TOKEN=seu_token_aqui")
        return
    
    # Inicializar API
    logger.info("\n🔗 Conectando à API Acessórias...")
    api = AcessoriasAPI(api_token)
    
    # Resultados consolidados
    resultados = []
    total_processos = 0
    total_andamento = 0
    total_concluidos = 0
    
    # Processar cada tipo de processo
    for idx, tipo_processo in enumerate(TIPOS_PROCESSOS, 1):
        logger.info(f"\n\n{'#'*70}")
        logger.info(f"TIPO {idx}/{len(TIPOS_PROCESSOS)}: {tipo_processo['nome']}")
        logger.info(f"{'#'*70}")
        
        try:
            # Buscar processos
            processos, stats = buscar_processos_por_tipo(api, tipo_processo, logger)
            
            # Processar e exportar
            if processos:
                caminho_excel = processar_e_exportar(processos, tipo_processo, stats, logger)
                
                resultados.append({
                    'tipo': tipo_processo['nome'],
                    'arquivo': caminho_excel,
                    'stats': stats
                })
                
                total_processos += stats['total']
                total_andamento += stats['andamento']
                total_concluidos += stats['concluidos']
            else:
                logger.warning(f"⚠️ Nenhum processo encontrado para: {tipo_processo['nome']}")
                
        except Exception as e:
            logger.error(f"❌ ERRO ao processar {tipo_processo['nome']}: {str(e)}", exc_info=True)
            continue
    
    # Resumo final
    logger.info("\n\n" + "="*70)
    logger.info("✅ PROCESSO CONCLUÍDO!")
    logger.info("="*70)
    
    logger.info(f"\n📊 ESTATÍSTICAS GERAIS:")
    logger.info(f"   Total de processos: {total_processos}")
    logger.info(f"   Em andamento: {total_andamento}")
    logger.info(f"   Concluídos: {total_concluidos}")
    logger.info(f"   Taxa de conclusão geral: {(total_concluidos/total_processos*100 if total_processos > 0 else 0):.1f}%")
    
    logger.info(f"\n📁 PLANILHAS GERADAS ({len(resultados)}):")
    for resultado in resultados:
        logger.info(f"\n   📄 {resultado['tipo']}:")
        logger.info(f"      Arquivo: {resultado['arquivo']}")
        logger.info(f"      Total: {resultado['stats']['total']} processos")
        logger.info(f"      Concluídos: {resultado['stats']['concluidos']} ({resultado['stats']['taxa_conclusao']:.1f}%)")
    
    logger.info(f"\n💡 PRÓXIMOS PASSOS:")
    logger.info(f"   1. Abra as planilhas geradas na pasta: output/planilhas/")
    logger.info(f"   2. Analise os dados de cada regime tributário")
    logger.info(f"   3. Envie prints das matrizes de cada processo para análise detalhada")
    logger.info(f"   4. Solicite criação do dashboard de gestão personalizado")
    
    logger.info("\n" + "="*70)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Processo interrompido pelo usuário")
    except Exception as e:
        logging.error(f"\n❌ ERRO FATAL: {str(e)}", exc_info=True)
        sys.exit(1)
