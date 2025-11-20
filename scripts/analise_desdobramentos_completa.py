"""
Análise Completa de Todos os Desdobramentos
Identificação de padrões e prioridades
"""

import pandas as pd
from pathlib import Path
from collections import Counter

print('='*100)
print('🔍 ANÁLISE PROFUNDA DE TODOS OS 736 DESDOBRAMENTOS')
print('='*100)

# Carregar todos os desdobramentos
planilhas_path = Path('output/planilhas')
todos_desd = []

for arquivo in planilhas_path.glob('*.xlsx'):
    if arquivo.name.startswith('~'):
        continue
    try:
        df = pd.read_excel(arquivo, 'PROCESSOS_DESDOBRAMENTOS')
        regime = arquivo.stem.split('_DadosBrutos')[0]
        df['REGIME'] = regime
        todos_desd.append(df)
    except Exception as e:
        print(f'Erro: {e}')
        continue

df_all = pd.concat(todos_desd, ignore_index=True)

print(f'\n📊 TOTAL: {len(df_all)} desdobramentos')
print(f'Empresas únicas: {df_all["PROC_ID"].nunique()}')
print(f'Regimes: {df_all["REGIME"].nunique()}')

print(f'\n🔝 TOP 10 PERGUNTAS MAIS FREQUENTES')
print('─'*100)
top_perguntas = df_all['DESDOBRAMENTO_NOME'].value_counts().head(10)
for i, (pergunta, count) in enumerate(top_perguntas.items(), 1):
    pct = count/len(df_all)*100
    print(f'{i:2d}. [{count:3d} | {pct:5.1f}%] {pergunta}')

print(f'\n📋 ANÁLISE DE ALTERNATIVAS (Top 5 Perguntas)')
print('─'*100)

for pergunta in top_perguntas.head(5).index:
    df_perg = df_all[df_all['DESDOBRAMENTO_NOME'] == pergunta]
    print(f'\n📌 {pergunta}')
    print(f'   Total: {len(df_perg)} empresas')
    
    # Alternativas disponíveis
    alternativas_unicas = df_perg['ALTERNATIVAS_DISPONIVEIS'].unique()
    if len(alternativas_unicas) == 1:
        print(f'   Alternativas: {alternativas_unicas[0]}')
    else:
        print(f'   ⚠️  Variações de alternativas: {len(alternativas_unicas)}')
        for alt in alternativas_unicas[:3]:
            print(f'      • {alt}')
    
    # Respostas dadas
    respondidos = df_perg[df_perg['DESDOBRAMENTO_STATUS'] == 'OK']
    if len(respondidos) > 0:
        print(f'   Respondidos: {len(respondidos)} ({len(respondidos)/len(df_perg)*100:.1f}%)')
        escolhas = respondidos['ALTERNATIVA_ESCOLHIDA'].value_counts()
        for escolha, count in escolhas.items():
            print(f'      ✅ {escolha}: {count}x')
    else:
        print(f'   ⏳ Nenhum respondido ainda')

print(f'\n🎯 ANÁLISE POR REGIME')
print('─'*100)

for regime in sorted(df_all['REGIME'].unique()):
    df_regime = df_all[df_all['REGIME'] == regime]
    perguntas_regime = df_regime['DESDOBRAMENTO_NOME'].value_counts()
    
    print(f'\n📁 {regime}')
    print(f'   Total desdobramentos: {len(df_regime)}')
    print(f'   Perguntas únicas: {df_regime["DESDOBRAMENTO_NOME"].nunique()}')
    print(f'   Top 3 perguntas:')
    for i, (perg, count) in enumerate(perguntas_regime.head(3).items(), 1):
        print(f'      {i}. {perg}: {count}x')

print(f'\n🔍 AÇÕES RESULTANTES (Quando respondido)')
print('─'*100)

df_resp = df_all[df_all['DESDOBRAMENTO_STATUS'] == 'OK']
if len(df_resp) > 0:
    acoes = df_resp['ACAO_TIPO'].value_counts()
    print(f'Total respondidos: {len(df_resp)}')
    print(f'\nTipos de ação:')
    for acao, count in acoes.items():
        pct = count/len(df_resp)*100
        print(f'   • {acao}: {count} ({pct:.1f}%)')
    
    print(f'\nTop 5 ações específicas:')
    acoes_nomes = df_resp['ACAO_NOME'].value_counts().head(5)
    for nome, count in acoes_nomes.items():
        print(f'   • {nome}: {count}x')

print(f'\n📊 PADRÕES DE ALTERNATIVAS')
print('─'*100)

# Contar quantas perguntas têm 2, 3, 4+ alternativas
alternativas_count = df_all.groupby('DESDOBRAMENTO_NOME')['ALTERNATIVAS_DISPONIVEIS'].first()
alternativas_split = alternativas_count.apply(lambda x: len(str(x).split(';')) if pd.notna(x) else 0)

print(f'Perguntas com 2 alternativas: {(alternativas_split == 2).sum()}')
print(f'Perguntas com 3 alternativas: {(alternativas_split == 3).sum()}')
print(f'Perguntas com 4+ alternativas: {(alternativas_split >= 4).sum()}')

# Exportar análise detalhada para Excel
print(f'\n💾 EXPORTANDO ANÁLISE DETALHADA...')
output_file = Path('output') / 'ANALISE_DESDOBRAMENTOS_COMPLETA.xlsx'

with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
    workbook = writer.book
    
    # Formato de cabeçalho
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#1F4E78',
        'font_color': 'white',
        'border': 1
    })
    
    # ABA 1: Resumo Geral
    resumo_data = []
    for pergunta, count in top_perguntas.items():
        df_p = df_all[df_all['DESDOBRAMENTO_NOME'] == pergunta]
        respondidos = len(df_p[df_p['DESDOBRAMENTO_STATUS'] == 'OK'])
        pendentes = len(df_p[df_p['DESDOBRAMENTO_STATUS'] == 'Pendente'])
        
        resumo_data.append({
            'Pergunta': pergunta,
            'Total': count,
            '% do Total': f'{count/len(df_all)*100:.1f}%',
            'Respondidos': respondidos,
            'Pendentes': pendentes,
            '% Respondido': f'{respondidos/count*100:.1f}%' if count > 0 else '0%'
        })
    
    df_resumo = pd.DataFrame(resumo_data)
    df_resumo.to_excel(writer, sheet_name='RESUMO_GERAL', index=False)
    
    worksheet = writer.sheets['RESUMO_GERAL']
    for col_num, value in enumerate(df_resumo.columns.values):
        worksheet.write(0, col_num, value, header_format)
    worksheet.set_column('A:A', 60)
    worksheet.set_column('B:F', 15)
    
    # ABA 2: Por Regime
    regime_data = []
    for regime in sorted(df_all['REGIME'].unique()):
        df_r = df_all[df_all['REGIME'] == regime]
        respondidos = len(df_r[df_r['DESDOBRAMENTO_STATUS'] == 'OK'])
        
        regime_data.append({
            'Regime': regime,
            'Total Desdobramentos': len(df_r),
            'Perguntas Únicas': df_r['DESDOBRAMENTO_NOME'].nunique(),
            'Respondidos': respondidos,
            'Pendentes': len(df_r) - respondidos,
            '% Respondido': f'{respondidos/len(df_r)*100:.1f}%' if len(df_r) > 0 else '0%'
        })
    
    df_regime_resumo = pd.DataFrame(regime_data)
    df_regime_resumo.to_excel(writer, sheet_name='POR_REGIME', index=False)
    
    worksheet = writer.sheets['POR_REGIME']
    for col_num, value in enumerate(df_regime_resumo.columns.values):
        worksheet.write(0, col_num, value, header_format)
    worksheet.set_column('A:A', 40)
    worksheet.set_column('B:F', 18)
    
    # ABA 3: Todas as perguntas únicas com alternativas
    perguntas_unicas = df_all.groupby('DESDOBRAMENTO_NOME').agg({
        'ALTERNATIVAS_DISPONIVEIS': 'first',
        'DESDOBRAMENTO_STATUS': 'count'
    }).reset_index()
    perguntas_unicas.columns = ['Pergunta', 'Alternativas', 'Frequência']
    perguntas_unicas = perguntas_unicas.sort_values('Frequência', ascending=False)
    
    perguntas_unicas.to_excel(writer, sheet_name='TODAS_PERGUNTAS', index=False)
    
    worksheet = writer.sheets['TODAS_PERGUNTAS']
    for col_num, value in enumerate(perguntas_unicas.columns.values):
        worksheet.write(0, col_num, value, header_format)
    worksheet.set_column('A:A', 60)
    worksheet.set_column('B:B', 50)
    worksheet.set_column('C:C', 15)

print(f'✅ Arquivo criado: {output_file}')

print(f'\n' + '='*100)
print('✅ ANÁLISE COMPLETA')
print('='*100)
