"""
Exemplos práticos de consulta de desdobramentos
"""

import pandas as pd
from pathlib import Path

print('='*100)
print('🔍 EXEMPLO 1: DESDOBRAMENTOS SOBRE DIRB')
print('='*100)

# Carregar arquivo
arquivo = Path(r'c:\acessorias processos\output\planilhas\LucroPresumido_Comercio_DadosBrutos_20251117_203642.xlsx')
df = pd.read_excel(arquivo, 'PROCESSOS_DESDOBRAMENTOS')

# Filtrar DIRB
df_dirb = df[df['DESDOBRAMENTO_NOME'].str.contains('DIRB', case=False, na=False)]

print(f'\nTotal de empresas com pergunta DIRB: {len(df_dirb)}')
respondidos = df_dirb[df_dirb['DESDOBRAMENTO_STATUS'] == 'OK']
pendentes = df_dirb[df_dirb['DESDOBRAMENTO_STATUS'] == 'Pendente']

print(f'✅ Respondidos: {len(respondidos)}')
print(f'⏳ Pendentes: {len(pendentes)}')

if len(respondidos) > 0:
    print('\n📊 RESPOSTAS DADAS:')
    for _, row in respondidos.iterrows():
        print(f'   🏢 {row["EMPRESA"]}')
        print(f'      ➡️  Escolheu: {row["ALTERNATIVA_ESCOLHIDA"]}')
        if pd.notna(row['ACAO_NOME']):
            print(f'      🎯 Ação: {row["ACAO_TIPO"]} - {row["ACAO_NOME"]}')
        print()

print('\n' + '='*100)
print('🔍 EXEMPLO 2: DESDOBRAMENTOS SOBRE REINF')
print('='*100)

df_reinf = df[df['DESDOBRAMENTO_NOME'].str.contains('REINF', case=False, na=False)]
print(f'\nTotal de empresas com pergunta REINF: {len(df_reinf)}')

respondidos_reinf = df_reinf[df_reinf['DESDOBRAMENTO_STATUS'] == 'OK']
if len(respondidos_reinf) > 0:
    print('\n📊 RESPOSTAS SOBRE REINF:')
    escolhas = respondidos_reinf['ALTERNATIVA_ESCOLHIDA'].value_counts()
    for escolha, count in escolhas.items():
        pct = count / len(respondidos_reinf) * 100
        print(f'   • "{escolha}": {count} empresas ({pct:.1f}%)')
        
        # Mostrar exemplos
        empresas_exemplo = respondidos_reinf[respondidos_reinf['ALTERNATIVA_ESCOLHIDA'] == escolha]['EMPRESA'].head(3)
        for emp in empresas_exemplo:
            print(f'      - {emp}')

print('\n' + '='*100)
print('🔍 EXEMPLO 3: DESDOBRAMENTOS SOBRE FATURAMENTO')
print('='*100)

df_fatur = df[df['DESDOBRAMENTO_NOME'].str.contains('Faturamento', case=False, na=False)]
print(f'\nTotal de empresas com pergunta Faturamento: {len(df_fatur)}')

respondidos_fatur = df_fatur[df_fatur['DESDOBRAMENTO_STATUS'] == 'OK']
if len(respondidos_fatur) > 0:
    print('\n📊 RESPOSTAS SOBRE FATURAMENTO:')
    escolhas = respondidos_fatur['ALTERNATIVA_ESCOLHIDA'].value_counts()
    for escolha, count in escolhas.items():
        pct = count / len(respondidos_fatur) * 100
        print(f'   • "{escolha}": {count} empresas ({pct:.1f}%)')

print('\n' + '='*100)
print('📊 VISÃO CONSOLIDADA - TODAS AS PLANILHAS')
print('='*100)

# Carregar todas as planilhas
planilhas_path = Path(r'c:\acessorias processos\output\planilhas')
todos_desdobramentos = []

for arquivo in planilhas_path.glob('*.xlsx'):
    # Ignorar arquivos temporários do Excel
    if arquivo.name.startswith('~$'):
        continue
    
    try:
        df_temp = pd.read_excel(arquivo, 'PROCESSOS_DESDOBRAMENTOS')
        regime = arquivo.stem.split('_DadosBrutos')[0]
        df_temp['REGIME'] = regime
        todos_desdobramentos.append(df_temp)
    except PermissionError:
        print(f'⚠️  Ignorando arquivo aberto: {arquivo.name}')
        continue

df_todos = pd.concat(todos_desdobramentos, ignore_index=True)

print(f'\n📊 TOTAL GERAL: {len(df_todos)} desdobramentos')
print(f'   ✅ Respondidos: {len(df_todos[df_todos["DESDOBRAMENTO_STATUS"] == "OK"])}')
print(f'   ⏳ Pendentes: {len(df_todos[df_todos["DESDOBRAMENTO_STATUS"] == "Pendente"])}')

print('\n🔝 TOP 5 PERGUNTAS MAIS FREQUENTES:')
top_perguntas = df_todos['DESDOBRAMENTO_NOME'].value_counts().head(5)
for i, (pergunta, count) in enumerate(top_perguntas.items(), 1):
    print(f'   {i}. {pergunta}: {count} vezes')

print('\n🎯 ALTERNATIVAS MAIS ESCOLHIDAS (GERAL):')
df_respondidos = df_todos[df_todos['DESDOBRAMENTO_STATUS'] == 'OK']
if len(df_respondidos) > 0:
    escolhas_geral = df_respondidos['ALTERNATIVA_ESCOLHIDA'].value_counts().head(10)
    for escolha, count in escolhas_geral.items():
        pct = count / len(df_respondidos) * 100
        print(f'   • "{escolha}": {count} vezes ({pct:.1f}%)')

print('\n' + '='*100)
