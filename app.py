"""
Dashboard Web - Gestão de Processos Contábeis
Competência 10/2025
"""

from flask import Flask, render_template, jsonify
import pandas as pd
import json
from pathlib import Path
from datetime import datetime

app = Flask(__name__)

# Configurações
DATA_DIR = Path(__file__).parent / 'data' / 'raw'
OUTPUT_DIR = Path(__file__).parent / 'output' / 'planilhas'

def carregar_dados():
    """Carrega todos os dados dos 5 regimes"""
    dados = {}
    total_processos = 0
    
    # Busca TODOS os arquivos Excel que existem no diretório
    import glob
    excel_files = list(OUTPUT_DIR.glob('*.xlsx'))
    
    print(f"\n🔍 Buscando arquivos Excel em: {OUTPUT_DIR}")
    print(f"📁 Encontrados {len(excel_files)} arquivos:")
    for f in excel_files:
        print(f"   - {f.name}")
    
    # Mapeia os arquivos encontrados para regimes
    regime_mapping = {
        'SimplesNacional': 'SimplesNacional',
        'LucroPresumido': 'Lucro Presumido',
        'LucroReal': 'Lucro Real',
    }
    
    for excel_file in excel_files:
        try:
            # Identifica o regime pelo nome do arquivo
            nome_arquivo = excel_file.stem.split('_')[0]  # Pega primeira parte antes do _
            
            # Lê o arquivo Excel - tenta diferentes abas
            abas_possiveis = ['PROCESSOS_GERAL', 'PROCESSOS', 'processos']
            df = None
            
            for aba in abas_possiveis:
                try:
                    df = pd.read_excel(excel_file, sheet_name=aba)
                    print(f"✅ Carregado {excel_file.name} (aba: {aba}) - {len(df)} processos")
                    break
                except:
                    continue
            
            if df is not None and not df.empty:
                dados[nome_arquivo] = df
                total_processos += len(df)
            
        except Exception as e:
            print(f"❌ Erro ao carregar {excel_file.name}: {e}")
    
    print(f"\n📊 Total de processos carregados: {total_processos}")
    return dados, total_processos

@app.route('/')
def index():
    """Página principal do dashboard"""
    dados, total_processos = carregar_dados()
    
    # Estatísticas gerais
    stats = {
        'total_processos': total_processos,
        'competencia': '10/2025',
        'regimes': len(dados),
        'ultima_atualizacao': datetime.now().strftime('%d/%m/%Y %H:%M')
    }
    
    # Dados por regime
    regimes_stats = []
    for nome, df in dados.items():
        if not df.empty:
            regimes_stats.append({
                'nome': nome.replace('_', ' '),
                'total': len(df),
                'percentual': round(len(df) / total_processos * 100, 1) if total_processos > 0 else 0
            })
    
    return render_template('dashboard.html', stats=stats, regimes=regimes_stats)

@app.route('/api/dados')
def api_dados():
    """API para retornar dados em JSON"""
    dados, total_processos = carregar_dados()
    
    resultado = {
        'total_processos': total_processos,
        'competencia': '10/2025',
        'regimes': {}
    }
    
    for nome, df in dados.items():
        if not df.empty:
            resultado['regimes'][nome] = {
                'total': len(df),
                'processos': df.to_dict('records')
            }
    
    return jsonify(resultado)

@app.route('/api/regime/<regime>')
def api_regime(regime):
    """API para retornar dados de um regime específico"""
    dados, _ = carregar_dados()
    
    if regime in dados and not dados[regime].empty:
        return jsonify({
            'regime': regime,
            'total': len(dados[regime]),
            'processos': dados[regime].to_dict('records')
        })
    else:
        return jsonify({'error': 'Regime não encontrado'}), 404

if __name__ == '__main__':
    print("\n" + "="*70)
    print(" 🚀 DASHBOARD WEB - GESTÃO DE PROCESSOS CONTÁBEIS")
    print("="*70)
    print(f" Competência: 10/2025 (Outubro 2025)")
    print(f" URL: http://localhost:5000")
    print(f" API: http://localhost:5000/api/dados")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
