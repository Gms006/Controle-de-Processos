"""
Script de monitoramento do progresso da sincronização
Execute este script para ver o progresso em tempo real
"""

import sqlite3
import time
from datetime import datetime

def monitorar():
    print("=" * 80)
    print("MONITORAMENTO DA SINCRONIZAÇÃO")
    print("Pressione Ctrl+C para parar")
    print("=" * 80)
    
    ultima_contagem = 0
    inicio = datetime.now()
    
    try:
        while True:
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            
            # Total de processos
            c.execute('SELECT COUNT(*) FROM processos')
            total = c.fetchone()[0]
            
            # Por regime
            c.execute('''
                SELECT 
                    regime_tributario, 
                    COUNT(*) as total,
                    SUM(CASE WHEN status = 'CONCLUIDO' THEN 1 ELSE 0 END) as concluidos
                FROM processos
                GROUP BY regime_tributario
                ORDER BY regime_tributario
            ''')
            regimes = c.fetchall()
            
            # Total de empresas
            c.execute('SELECT COUNT(DISTINCT empresa_id) FROM processos')
            empresas = c.fetchone()[0]
            
            # Total de passos
            c.execute('SELECT COUNT(*) FROM passos')
            passos = c.fetchone()[0]
            
            # Total de desdobramentos
            c.execute('SELECT COUNT(*) FROM desdobramentos')
            desdobramentos = c.fetchone()[0]
            
            conn.close()
            
            # Calcular velocidade
            novos = total - ultima_contagem
            tempo_decorrido = (datetime.now() - inicio).total_seconds()
            velocidade = total / tempo_decorrido if tempo_decorrido > 0 else 0
            
            # Limpar tela (Windows)
            print('\033[2J\033[H', end='')
            
            # Exibir progresso
            print("=" * 80)
            print(f"PROGRESSO DA SINCRONIZAÇÃO - {datetime.now().strftime('%H:%M:%S')}")
            print("=" * 80)
            print(f"\n📊 RESUMO GERAL:")
            print(f"   Processos: {total}/211 ({total/211*100:.1f}%)")
            print(f"   Empresas: {empresas}")
            print(f"   Passos: {passos}")
            print(f"   Desdobramentos: {desdobramentos}")
            print(f"\n⏱️  PERFORMANCE:")
            print(f"   Tempo decorrido: {int(tempo_decorrido)}s")
            print(f"   Velocidade: {velocidade:.2f} processos/s")
            print(f"   Novos (última atualização): +{novos}")
            
            if regimes:
                print(f"\n📋 POR REGIME:")
                for regime, total_regime, concluidos in regimes:
                    pct_regime = concluidos / total_regime * 100 if total_regime > 0 else 0
                    print(f"   {regime}: {total_regime} processos ({concluidos} concluídos - {pct_regime:.1f}%)")
            
            # Barra de progresso
            pct = total / 211 * 100
            barra_tamanho = 50
            barra_preenchida = int(barra_tamanho * total / 211)
            barra = '█' * barra_preenchida + '░' * (barra_tamanho - barra_preenchida)
            print(f"\n📈 PROGRESSO GERAL:")
            print(f"   [{barra}] {pct:.1f}%")
            
            print("\n" + "=" * 80)
            print("Atualizando a cada 5 segundos... (Ctrl+C para parar)")
            
            ultima_contagem = total
            
            # Aguardar 5 segundos
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n\n✅ Monitoramento encerrado.")
    except Exception as e:
        print(f"\n❌ Erro: {e}")

if __name__ == '__main__':
    monitorar()
