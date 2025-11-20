"""
Buscar Processos - Simples Nacional
Script principal para buscar e analisar processos do Simples Nacional
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import os

# Adicionar diretório raiz ao path
sys.path.append(str(Path(__file__).parent))

from api_client import AcessoriasAPI
from processador_processos import ProcessadorProcessos
from exportador_excel import ExportadorExcel


def setup_logging():
    """Configura o sistema de logs"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / "app.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    logging.info("=" * 70)
    logging.info("INICIANDO BUSCA DE PROCESSOS - SIMPLES NACIONAL")
    logging.info("=" * 70)


def carregar_configuracoes():
    """Carrega configurações e credenciais"""
    # Carregar .env
    load_dotenv()
    
    api_token = os.getenv('API_TOKEN')
    
    if not api_token or api_token == 'seu_token_secreto_aqui':
        logging.error("❌ API_TOKEN não configurado!")
        logging.error("Por favor, edite o arquivo .env e adicione seu token da API")
        sys.exit(1)
    
    logging.info("✓ Configurações carregadas")
    return api_token


def buscar_processos_simples_nacional(api: AcessoriasAPI):
    """
    Busca todos os processos de Simples Nacional
    Separando em: Concluídos e Em Andamento
    """
    logging.info("\n" + "=" * 70)
    logging.info("ETAPA 1: BUSCAR PROCESSOS DA API")
    logging.info("=" * 70)
    
    processos_todos = []
    
    # Buscar processos em ANDAMENTO
    logging.info("\n🔍 Buscando processos EM ANDAMENTO...")
    processos_andamento = api.get_all_processes_paginated(
        proc_status="A",
        proc_nome="Simples Nacional",
        with_details=True  # IMPORTANTE: buscar detalhes completos (ProcPassos)
    )
    
    if processos_andamento:
        logging.info(f"✓ {len(processos_andamento)} processos em andamento encontrados")
        processos_todos.extend(processos_andamento)
    else:
        logging.warning("⚠️  Nenhum processo em andamento encontrado")
    
    # Buscar processos CONCLUÍDOS
    logging.info("\n🔍 Buscando processos CONCLUÍDOS...")
    processos_concluidos = api.get_all_processes_paginated(
        proc_status="C",
        proc_nome="Simples Nacional",
        with_details=True  # IMPORTANTE: buscar detalhes completos (ProcPassos)
    )
    
    if processos_concluidos:
        logging.info(f"✓ {len(processos_concluidos)} processos concluídos encontrados")
        processos_todos.extend(processos_concluidos)
    else:
        logging.warning("⚠️  Nenhum processo concluído encontrado")
    
    # Salvar dados brutos
    if processos_todos:
        salvar_dados_brutos(processos_todos)
    
    return processos_todos


def salvar_dados_brutos(processos: list):
    """Salva dados brutos em JSON para backup"""
    data_dir = Path("data/raw")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = data_dir / f"processos_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(processos, f, ensure_ascii=False, indent=2)
    
    logging.info(f"✓ Dados brutos salvos: {filename}")


def processar_dados(processos: list):
    """Processa os dados e gera DataFrames"""
    logging.info("\n" + "=" * 70)
    logging.info("ETAPA 2: PROCESSAR DADOS")
    logging.info("=" * 70)
    
    processador = ProcessadorProcessos()
    df_geral, df_passos, df_desdobramentos = processador.processar_lista_processos(processos)
    
    # Gerar estatísticas
    stats = processador.gerar_estatisticas()
    
    logging.info("\n📊 ESTATÍSTICAS:")
    logging.info(f"  Total de processos: {stats['total_processos']}")
    logging.info(f"  Concluídos: {stats['total_concluidos']}")
    logging.info(f"  Em andamento: {stats['total_andamento']}")
    logging.info(f"  Taxa de conclusão: {stats['taxa_conclusao']:.1f}%")
    
    return df_geral, df_passos, df_desdobramentos, stats


def exportar_planilha(df_geral, df_passos, df_desdobramentos):
    """Exporta dados para planilha Excel"""
    logging.info("\n" + "=" * 70)
    logging.info("ETAPA 3: GERAR PLANILHA EXCEL")
    logging.info("=" * 70)
    
    exportador = ExportadorExcel()
    filepath = exportador.exportar_dados_brutos(df_geral, df_passos, df_desdobramentos)
    
    return filepath


def main():
    """Função principal"""
    try:
        # Setup
        setup_logging()
        api_token = carregar_configuracoes()
        
        # Conectar à API
        logging.info("\n🔗 Conectando à API Acessórias...")
        api = AcessoriasAPI(api_token)
        
        # Buscar processos
        processos = buscar_processos_simples_nacional(api)
        
        if not processos:
            logging.warning("\n⚠️  Nenhum processo encontrado!")
            logging.warning("Verifique se:")
            logging.warning("  1. O token da API está correto")
            logging.warning("  2. Existem processos de Simples Nacional no sistema")
            logging.warning("  3. Você tem permissão para acessar os processos")
            return
        
        # Processar dados
        df_geral, df_passos, df_desdobramentos, stats = processar_dados(processos)
        
        # Exportar planilha
        filepath = exportar_planilha(df_geral, df_passos, df_desdobramentos)
        
        # Resumo final
        logging.info("\n" + "=" * 70)
        logging.info("✅ PROCESSO CONCLUÍDO COM SUCESSO!")
        logging.info("=" * 70)
        logging.info(f"\n📁 Planilha gerada: {filepath}")
        logging.info(f"\n📊 Resumo:")
        logging.info(f"  • Total de processos: {stats['total_processos']}")
        logging.info(f"  • Concluídos: {stats['total_concluidos']} ({stats['taxa_conclusao']:.1f}%)")
        logging.info(f"  • Em andamento: {stats['total_andamento']}")
        logging.info(f"\n💡 Próximos passos:")
        logging.info(f"  1. Abra a planilha: {filepath}")
        logging.info(f"  2. Analise as 3 abas:")
        logging.info(f"     - PROCESSOS_GERAL (visão consolidada)")
        logging.info(f"     - PROCESSOS_PASSOS (detalhamento)")
        logging.info(f"     - PROCESSOS_DESDOBRAMENTOS (decisões)")
        logging.info(f"  3. Valide se os dados estão corretos")
        logging.info(f"  4. Me dê feedback para próximas melhorias!")
        
    except Exception as e:
        logging.error(f"\n❌ ERRO: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
