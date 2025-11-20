"""
Script para continuar sincronização - Apenas SimplesNacional
"""

import sys
from pathlib import Path

# Adicionar paths
sys.path.insert(0, str(Path(__file__).parent))
backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

from sincronizar_banco import SincronizadorProfissional, TIPOS_PROCESSOS

def main():
    print("=" * 80)
    print("CONTINUANDO SINCRONIZAÇÃO - SIMPLES NACIONAL")
    print("=" * 80)
    
    sync = SincronizadorProfissional()
    
    # Buscar apenas SimplesNacional
    tipo = TIPOS_PROCESSOS[0]  # SimplesNacional é o primeiro
    
    print(f"\n📋 Buscando processos: {tipo['nome']}")
    print(f"   Código: {tipo['codigo']}")
    print(f"   {tipo['descricao']}")
    print("-" * 80)
    
    try:
        # Buscar processos
        processos = sync.buscar_processos_por_tipo(tipo)
        
        print(f"\n✅ {len(processos)} processos encontrados!")
        print(f"📊 Salvando no banco de dados...")
        print("-" * 80)
        
        # Salvar no banco
        sync.salvar_no_banco(processos, tipo['codigo'])
        
        print(f"\n✅ CONCLUÍDO!")
        print(f"   Empresas novas: {sync.stats['empresas_novas']}")
        print(f"   Empresas atualizadas: {sync.stats['empresas_atualizadas']}")
        print(f"   Processos novos: {sync.stats['processos_novos']}")
        print(f"   Processos atualizados: {sync.stats['processos_atualizados']}")
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
    finally:
        sync.db.close()
    
    print("\n" + "=" * 80)
    print("SINCRONIZAÇÃO FINALIZADA")
    print("=" * 80)

if __name__ == '__main__':
    main()
