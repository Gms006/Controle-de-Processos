"""
Script de Sincronização para GitHub Actions
Atualiza o banco de dados SQLite com dados da API Acessórias
"""
import os
import sys
from pathlib import Path

# Adicionar o diretório streamlit_app ao path
streamlit_path = Path(__file__).parent.parent.parent / "streamlit_app"
sys.path.insert(0, str(streamlit_path))

from utils.sync_manager import SyncManager
from utils.database import DatabaseManager

def main():
    """Executa a sincronização"""
    print("=" * 70)
    print("🔄 SINCRONIZAÇÃO AUTOMÁTICA - GitHub Actions")
    print("=" * 70)
    
    # Obter credenciais das variáveis de ambiente
    api_token = os.environ.get('ACESSORIAS_API_TOKEN')
    api_url = os.environ.get('ACESSORIAS_API_URL', 'https://api.acessorias.com')
    
    if not api_token:
        print("❌ ERRO: ACESSORIAS_API_TOKEN não configurado!")
        print("Configure o secret no GitHub: Settings > Secrets > Actions")
        sys.exit(1)
    
    print(f"✓ Token configurado")
    print(f"✓ API URL: {api_url}")
    print()
    
    # Configurar caminho do banco de dados
    db_path = streamlit_path / "data" / "processos.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"📂 Banco de dados: {db_path}")
    print()
    
    # Inicializar banco de dados (criar tabelas se necessário)
    print("🔧 Inicializando banco de dados...")
    db_manager = DatabaseManager(db_path=str(db_path))
    print("✓ Banco inicializado")
    print()
    
    # Criar SyncManager
    sync_manager = SyncManager(
        api_token=api_token,
        api_url=api_url,
        db_path=str(db_path)
    )
    
    try:
        # Executar sincronização
        print("🔄 Iniciando sincronização...")
        resultado = sync_manager.sync_processos()
        
        print()
        print("=" * 70)
        print("✅ SINCRONIZAÇÃO CONCLUÍDA!")
        print("=" * 70)
        print(f"📊 Total de processos: {resultado['total_processos']}")
        print(f"🆕 Novos: {resultado['processos_novos']}")
        print(f"🔄 Atualizados: {resultado['processos_atualizados']}")
        print(f"⏱️  Tempo: {resultado['tempo_execucao']}s")
        print("=" * 70)
        
        return 0
    
    except Exception as e:
        print()
        print("=" * 70)
        print("❌ ERRO NA SINCRONIZAÇÃO")
        print("=" * 70)
        print(f"Erro: {str(e)}")
        print()
        import traceback
        traceback.print_exc()
        print("=" * 70)
        
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
