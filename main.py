"""
Script Principal - Inicialização
Ponto de entrada para execução do projeto
"""

from pathlib import Path
import sys

# Adiciona o diretório scripts ao path
sys.path.append(str(Path(__file__).parent / "scripts"))

from buscar_processos_simples_nacional import main

if __name__ == "__main__":
    print("=" * 60)
    print("  ANÁLISE DE PROCESSOS - API ACESSÓRIAS")
    print("  Foco: Simples Nacional - Mensal")
    print("=" * 60)
    print()
    
    main()
