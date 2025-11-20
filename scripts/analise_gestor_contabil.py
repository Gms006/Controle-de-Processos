"""
Análise Profunda - Visão do Gestor Contábil
Análise completa de processos, obrigações e desempenho
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

print('='*100)
print('📊 ANÁLISE PROFUNDA - VISÃO DO GESTOR CONTÁBIL')
print('='*100)

# Carregar todos os processos
planilhas_path = Path(r'c:\acessorias processos\output\planilhas')
todos_processos = []
todos_passos = []
todos_desdobramentos = []

for arquivo in planilhas_path.glob('*.xlsx'):
    if arquivo.name.startswith('~'):
        continue
    try:
        df_geral = pd.read_excel(arquivo, 'PROCESSOS_GERAL')
        df_passos = pd.read_excel(arquivo, 'PROCESSOS_PASSOS')
        df_desd = pd.read_excel(arquivo, 'PROCESSOS_DESDOBRAMENTOS')
        regime = arquivo.stem.split('_DadosBrutos')[0]
        df_geral['REGIME'] = regime
        df_passos['REGIME'] = regime
        df_desd['REGIME'] = regime
        todos_processos.append(df_geral)
        todos_passos.append(df_passos)
        todos_desdobramentos.append(df_desd)
    except Exception as e:
        print(f'Erro ao carregar {arquivo.name}: {e}')
        continue

df_proc = pd.concat(todos_processos, ignore_index=True)
df_pass = pd.concat(todos_passos, ignore_index=True)
df_desd = pd.concat(todos_desdobramentos, ignore_index=True)

print(f'\n📈 VISÃO GERAL DO ESCRITÓRIO')
print('─'*100)
print(f'Total de Empresas em Processamento: {len(df_proc)}')
print(f'Total de Regimes Tributários: {df_proc["REGIME"].nunique()}')
print(f'Total de Passos Executados: {len(df_pass)}')
print(f'Total de Desdobramentos: {len(df_desd)}')

print(f'\n📊 DISTRIBUIÇÃO POR REGIME')
print('─'*100)
for regime in sorted(df_proc['REGIME'].unique()):
    total = len(df_proc[df_proc['REGIME'] == regime])
    concluidos = len(df_proc[(df_proc['REGIME'] == regime) & (df_proc['STATUS'] == 'Concluído')])
    taxa = (concluidos/total*100) if total > 0 else 0
    print(f'{regime:40s}: {total:3d} empresas ({concluidos:2d} concluídas = {taxa:5.1f}%)')

print(f'\n⏱️  TEMPO DE PROCESSAMENTO')
print('─'*100)
df_concluidos = df_proc[df_proc['STATUS'] == 'Concluído']
if len(df_concluidos) > 0:
    print(f'Média de dias (concluídos): {df_concluidos["DIAS_CORRIDOS"].mean():.1f} dias')
    print(f'Mínimo: {df_concluidos["DIAS_CORRIDOS"].min()} dias')
    print(f'Máximo: {df_concluidos["DIAS_CORRIDOS"].max()} dias')
else:
    print('Nenhum processo concluído ainda')

df_andamento = df_proc[df_proc['STATUS'] == 'Em andamento']
if len(df_andamento) > 0:
    print(f'\nTempo médio em andamento: {df_andamento["DIAS_CORRIDOS"].mean():.1f} dias')
    print(f'Máximo em andamento: {df_andamento["DIAS_CORRIDOS"].max()} dias')

print(f'\n📋 PRINCIPAIS TIPOS DE PASSOS')
print('─'*100)
tipos_passos = df_pass['PASSO_TIPO'].value_counts()
for tipo, count in tipos_passos.items():
    pct = count/len(df_pass)*100
    print(f'{tipo:25s}: {count:4d} ({pct:5.1f}%)')

print(f'\n⚠️  STATUS DOS PASSOS')
print('─'*100)
status_passos = df_pass['PASSO_STATUS'].value_counts()
for status, count in status_passos.items():
    pct = count/len(df_pass)*100
    print(f'{status:15s}: {count:4d} ({pct:5.1f}%)')

print(f'\n🔍 ANÁLISE DE OBRIGAÇÕES ACESSÓRIAS')
print('─'*100)

# Buscar obrigações específicas nos passos
obrigacoes = {
    'EFD REINF': df_pass[df_pass['PASSO_NOME'].str.contains('REINF', case=False, na=False)],
    'EFD Contribuições': df_pass[df_pass['PASSO_NOME'].str.contains('Contribui', case=False, na=False)],
    'DIFAL': df_pass[df_pass['PASSO_NOME'].str.contains('DIFAL', case=False, na=False)],
    'ICMS': df_pass[df_pass['PASSO_NOME'].str.contains('ICMS', case=False, na=False)],
    'MIT': df_pass[df_pass['PASSO_NOME'].str.contains('MIT', case=False, na=False)],
    'PIS/COFINS': df_pass[df_pass['PASSO_NOME'].str.contains('PIS|COFINS', case=False, na=False)],
    'SPED': df_pass[df_pass['PASSO_NOME'].str.contains('SPED', case=False, na=False)],
}

for obrig, df_obrig in obrigacoes.items():
    if len(df_obrig) > 0:
        ok = len(df_obrig[df_obrig['PASSO_STATUS'] == 'OK'])
        pendente = len(df_obrig[df_obrig['PASSO_STATUS'] == 'Pendente'])
        empresas_unicas = df_obrig['PROC_ID'].nunique()
        print(f'{obrig:20s}: {empresas_unicas:3d} empresas | {len(df_obrig):3d} passos (OK: {ok:3d}, Pendente: {pendente:3d})')
    else:
        print(f'{obrig:20s}: Não encontrado nos passos')

print(f'\n💰 ANÁLISE DE FATURAMENTO (via Desdobramentos)')
print('─'*100)

# Análise de faturamento
df_fatur = df_desd[df_desd['DESDOBRAMENTO_NOME'].str.contains('faturamento', case=False, na=False)]
if len(df_fatur) > 0:
    respondidos = df_fatur[df_fatur['DESDOBRAMENTO_STATUS'] == 'OK']
    if len(respondidos) > 0:
        com_faturamento = respondidos[respondidos['ALTERNATIVA_ESCOLHIDA'].str.contains('Sim', case=False, na=False)]
        sem_faturamento = respondidos[respondidos['ALTERNATIVA_ESCOLHIDA'].str.contains('Não', case=False, na=False)]
        
        print(f'Total de empresas questionadas: {df_fatur["PROC_ID"].nunique()}')
        print(f'Respondidos: {len(respondidos)}')
        print(f'  ✅ COM faturamento: {len(com_faturamento)} empresas')
        print(f'  ❌ SEM faturamento: {len(sem_faturamento)} empresas')
        print(f'  ⏳ Aguardando resposta: {len(df_fatur) - len(respondidos)}')
    else:
        print('Nenhuma resposta sobre faturamento ainda')
else:
    print('Desdobramento de faturamento não encontrado')

print(f'\n📊 ANÁLISE DE REINF (via Desdobramentos)')
print('─'*100)

df_reinf = df_desd[df_desd['DESDOBRAMENTO_NOME'].str.contains('REINF', case=False, na=False)]
if len(df_reinf) > 0:
    respondidos = df_reinf[df_reinf['DESDOBRAMENTO_STATUS'] == 'OK']
    if len(respondidos) > 0:
        obrigadas = respondidos[respondidos['ALTERNATIVA_ESCOLHIDA'].str.contains('Sim', case=False, na=False)]
        dispensadas = respondidos[respondidos['ALTERNATIVA_ESCOLHIDA'].str.contains('Não', case=False, na=False)]
        
        print(f'Total de empresas questionadas: {df_reinf["PROC_ID"].nunique()}')
        print(f'Respondidos: {len(respondidos)}')
        print(f'  ✅ OBRIGADAS (com fato gerador): {len(obrigadas)} empresas')
        print(f'  ❌ DISPENSADAS (sem fato gerador): {len(dispensadas)} empresas')
        print(f'  ⏳ Aguardando resposta: {len(df_reinf) - len(respondidos)}')
    else:
        print('Nenhuma resposta sobre REINF ainda')

print(f'\n📊 ANÁLISE DE DIRB (via Desdobramentos)')
print('─'*100)

df_dirb = df_desd[df_desd['DESDOBRAMENTO_NOME'].str.contains('DIRB', case=False, na=False)]
if len(df_dirb) > 0:
    respondidos = df_dirb[df_dirb['DESDOBRAMENTO_STATUS'] == 'OK']
    if len(respondidos) > 0:
        obrigadas = respondidos[respondidos['ALTERNATIVA_ESCOLHIDA'].str.contains('Sim', case=False, na=False)]
        dispensadas = respondidos[respondidos['ALTERNATIVA_ESCOLHIDA'].str.contains('Não', case=False, na=False)]
        
        print(f'Total de empresas questionadas: {df_dirb["PROC_ID"].nunique()}')
        print(f'Respondidos: {len(respondidos)}')
        print(f'  ✅ OBRIGADAS: {len(obrigadas)} empresas')
        print(f'  ❌ DISPENSADAS: {len(dispensadas)} empresas')
        print(f'  ⏳ Aguardando resposta: {len(df_dirb) - len(respondidos)}')

print(f'\n🚨 ALERTAS E PRIORIDADES')
print('─'*100)

# Processos mais antigos ainda em andamento
df_antigos = df_andamento.nlargest(10, 'DIAS_CORRIDOS')
if len(df_antigos) > 0:
    print(f'\n⚠️  TOP 10 PROCESSOS MAIS ANTIGOS EM ANDAMENTO:')
    for _, proc in df_antigos.iterrows():
        print(f'  • {proc["EMPRESA"][:50]:50s} | {proc["REGIME"][:30]:30s} | {proc["DIAS_CORRIDOS"]:2d} dias | {proc["PORCENTAGEM"]:6.2f}%')

# Empresas com 0% de progresso
df_parados = df_andamento[df_andamento['PORCENTAGEM'] == 0]
if len(df_parados) > 0:
    print(f'\n🛑 PROCESSOS PARADOS (0% de progresso): {len(df_parados)} empresas')
    print(f'   Regimes afetados: {df_parados["REGIME"].value_counts().to_dict()}')

print(f'\n✅ EMPRESAS PRÓXIMAS DA CONCLUSÃO')
print('─'*100)

df_quase = df_andamento[df_andamento['PORCENTAGEM'] >= 75]
if len(df_quase) > 0:
    print(f'Total com 75%+ concluído: {len(df_quase)} empresas')
    for _, proc in df_quase.head(10).iterrows():
        print(f'  • {proc["EMPRESA"][:50]:50s} | {proc["PORCENTAGEM"]:6.2f}%')
else:
    print('Nenhuma empresa próxima da conclusão (75%+)')

print(f'\n' + '='*100)
print('📊 FIM DA ANÁLISE')
print('='*100)
