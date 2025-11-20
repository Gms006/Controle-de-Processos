"""
Script para consultar desdobramentos e suas respostas de forma organizada
Autor: Sistema de Gestão de Processos Acessórias
Data: 2025-11-17
"""

import pandas as pd
import glob
from pathlib import Path
from typing import Optional

def consultar_desdobramentos(
    tipo_processo: Optional[str] = None,
    empresa: Optional[str] = None,
    apenas_respondidos: bool = False,
    apenas_pendentes: bool = False
):
    """
    Consulta desdobramentos com filtros personalizados
    
    Args:
        tipo_processo: Filtrar por tipo (SimplesNacional, LucroPresumido_Servicos, etc)
        empresa: Filtrar por nome da empresa (busca parcial)
        apenas_respondidos: Mostrar apenas desdobramentos com status OK
        apenas_pendentes: Mostrar apenas desdobramentos pendentes
    """
    
    # Encontrar todos os arquivos Excel
    planilhas_path = Path("output/planilhas")
    arquivos = list(planilhas_path.glob("*.xlsx"))
    
    if not arquivos:
        print("❌ Nenhuma planilha encontrada em output/planilhas/")
        return
    
    # Filtrar por tipo de processo se especificado
    if tipo_processo:
        arquivos = [f for f in arquivos if tipo_processo in f.name]
    
    if not arquivos:
        print(f"❌ Nenhuma planilha encontrada para: {tipo_processo}")
        return
    
    print("="*100)
    print("📊 CONSULTA DE DESDOBRAMENTOS")
    print("="*100)
    
    total_geral = 0
    
    for arquivo in sorted(arquivos):
        regime = arquivo.stem.split('_DadosBrutos')[0]
        
        # Carregar dados
        df = pd.read_excel(arquivo, 'PROCESSOS_DESDOBRAMENTOS')
        
        # Aplicar filtros
        df_filtrado = df.copy()
        
        if empresa:
            df_filtrado = df_filtrado[df_filtrado['EMPRESA'].str.contains(empresa, case=False, na=False)]
        
        if apenas_respondidos:
            df_filtrado = df_filtrado[df_filtrado['DESDOBRAMENTO_STATUS'] == 'OK']
        
        if apenas_pendentes:
            df_filtrado = df_filtrado[df_filtrado['DESDOBRAMENTO_STATUS'] == 'Pendente']
        
        if len(df_filtrado) == 0:
            continue
        
        # Exibir informações do regime
        print(f"\n{'='*100}")
        print(f"📁 REGIME: {regime}")
        print(f"{'='*100}")
        
        respondidos = len(df_filtrado[df_filtrado['DESDOBRAMENTO_STATUS'] == 'OK'])
        pendentes = len(df_filtrado[df_filtrado['DESDOBRAMENTO_STATUS'] == 'Pendente'])
        
        print(f"✅ Respondidos: {respondidos}")
        print(f"⏳ Pendentes: {pendentes}")
        print(f"📊 Total: {len(df_filtrado)}")
        
        # Agrupar por empresa
        for empresa_nome in df_filtrado['EMPRESA'].unique():
            df_empresa = df_filtrado[df_filtrado['EMPRESA'] == empresa_nome]
            
            print(f"\n{'─'*100}")
            print(f"🏢 EMPRESA: {empresa_nome}")
            print(f"   CNPJ: {df_empresa.iloc[0]['CNPJ']}")
            print(f"   Total de desdobramentos: {len(df_empresa)}")
            print(f"{'─'*100}")
            
            # Ordenar por ordem do desdobramento
            df_empresa = df_empresa.sort_values('DESDOBRAMENTO_ORDEM')
            
            for _, row in df_empresa.iterrows():
                status_emoji = "✅" if row['DESDOBRAMENTO_STATUS'] == 'OK' else "⏳"
                
                print(f"\n  {status_emoji} Desdobramento {row['DESDOBRAMENTO_ORDEM']}: {row['DESDOBRAMENTO_NOME']}")
                print(f"     Status: {row['DESDOBRAMENTO_STATUS']}")
                print(f"     Alternativas disponíveis: {row['ALTERNATIVAS_DISPONIVEIS']}")
                
                if pd.notna(row['ALTERNATIVA_ESCOLHIDA']):
                    print(f"     ➡️  ESCOLHIDA: {row['ALTERNATIVA_ESCOLHIDA']}")
                    
                    if pd.notna(row['ACAO_TIPO']) and pd.notna(row['ACAO_NOME']):
                        print(f"     🎯 Ação resultante: {row['ACAO_TIPO']} - {row['ACAO_NOME']}")
                else:
                    print(f"     ⏳ Aguardando resposta...")
        
        total_geral += len(df_filtrado)
    
    print(f"\n{'='*100}")
    print(f"📊 TOTAL GERAL: {total_geral} desdobramentos encontrados")
    print(f"{'='*100}\n")


def estatisticas_desdobramentos():
    """
    Gera estatísticas gerais sobre os desdobramentos
    """
    
    planilhas_path = Path("output/planilhas")
    arquivos = list(planilhas_path.glob("*.xlsx"))
    
    if not arquivos:
        print("❌ Nenhuma planilha encontrada")
        return
    
    print("="*100)
    print("📊 ESTATÍSTICAS DE DESDOBRAMENTOS")
    print("="*100)
    
    dados_regimes = []
    
    for arquivo in sorted(arquivos):
        regime = arquivo.stem.split('_DadosBrutos')[0]
        df = pd.read_excel(arquivo, 'PROCESSOS_DESDOBRAMENTOS')
        
        total = len(df)
        respondidos = len(df[df['DESDOBRAMENTO_STATUS'] == 'OK'])
        pendentes = len(df[df['DESDOBRAMENTO_STATUS'] == 'Pendente'])
        taxa_resposta = (respondidos / total * 100) if total > 0 else 0
        
        dados_regimes.append({
            'Regime': regime,
            'Total': total,
            'Respondidos': respondidos,
            'Pendentes': pendentes,
            'Taxa Resposta (%)': f'{taxa_resposta:.1f}%'
        })
    
    df_stats = pd.DataFrame(dados_regimes)
    print(f"\n{df_stats.to_string(index=False)}\n")
    
    # Desdobramentos mais comuns
    print(f"\n{'='*100}")
    print("🔝 TOP 10 DESDOBRAMENTOS MAIS FREQUENTES")
    print(f"{'='*100}\n")
    
    todos_desdobramentos = []
    for arquivo in arquivos:
        df = pd.read_excel(arquivo, 'PROCESSOS_DESDOBRAMENTOS')
        todos_desdobramentos.append(df)
    
    df_todos = pd.concat(todos_desdobramentos, ignore_index=True)
    top_desdobramentos = df_todos['DESDOBRAMENTO_NOME'].value_counts().head(10)
    
    for i, (nome, count) in enumerate(top_desdobramentos.items(), 1):
        print(f"{i:2d}. {nome}: {count} ocorrências")
    
    # Alternativas mais escolhidas
    print(f"\n{'='*100}")
    print("🎯 ALTERNATIVAS MAIS ESCOLHIDAS")
    print(f"{'='*100}\n")
    
    df_respondidos = df_todos[df_todos['DESDOBRAMENTO_STATUS'] == 'OK']
    
    if len(df_respondidos) > 0:
        for desdobramento in df_respondidos['DESDOBRAMENTO_NOME'].unique():
            df_desd = df_respondidos[df_respondidos['DESDOBRAMENTO_NOME'] == desdobramento]
            escolhas = df_desd['ALTERNATIVA_ESCOLHIDA'].value_counts()
            
            print(f"\n📌 {desdobramento}")
            for escolha, count in escolhas.items():
                pct = count / len(df_desd) * 100
                print(f"   • {escolha}: {count} vezes ({pct:.1f}%)")
    else:
        print("⏳ Nenhum desdobramento respondido ainda")


def consultar_por_pergunta(pergunta: str):
    """
    Busca desdobramentos por palavra-chave na pergunta
    
    Args:
        pergunta: Palavra ou frase a buscar (ex: "DIRB", "REINF", "Faturamento")
    """
    
    planilhas_path = Path("output/planilhas")
    arquivos = list(planilhas_path.glob("*.xlsx"))
    
    if not arquivos:
        print("❌ Nenhuma planilha encontrada")
        return
    
    print("="*100)
    print(f"🔍 BUSCA: '{pergunta}'")
    print("="*100)
    
    encontrados = 0
    
    for arquivo in sorted(arquivos):
        regime = arquivo.stem.split('_DadosBrutos')[0]
        df = pd.read_excel(arquivo, 'PROCESSOS_DESDOBRAMENTOS')
        
        # Filtrar por palavra-chave
        df_filtrado = df[df['DESDOBRAMENTO_NOME'].str.contains(pergunta, case=False, na=False)]
        
        if len(df_filtrado) == 0:
            continue
        
        print(f"\n{'─'*100}")
        print(f"📁 {regime} - {len(df_filtrado)} ocorrências")
        print(f"{'─'*100}")
        
        # Estatísticas de respostas
        respondidos = df_filtrado[df_filtrado['DESDOBRAMENTO_STATUS'] == 'OK']
        
        if len(respondidos) > 0:
            print(f"\n✅ Respostas ({len(respondidos)} de {len(df_filtrado)}):")
            escolhas = respondidos['ALTERNATIVA_ESCOLHIDA'].value_counts()
            for escolha, count in escolhas.items():
                pct = count / len(respondidos) * 100
                print(f"   • {escolha}: {count} vezes ({pct:.1f}%)")
        
        pendentes = len(df_filtrado[df_filtrado['DESDOBRAMENTO_STATUS'] == 'Pendente'])
        if pendentes > 0:
            print(f"\n⏳ Pendentes: {pendentes}")
        
        encontrados += len(df_filtrado)
    
    print(f"\n{'='*100}")
    print(f"📊 Total encontrado: {encontrados} desdobramentos")
    print(f"{'='*100}\n")


if __name__ == "__main__":
    print("\n" + "="*100)
    print("🔍 SISTEMA DE CONSULTA DE DESDOBRAMENTOS")
    print("="*100 + "\n")
    
    while True:
        print("\nEscolha uma opção:")
        print("1. Estatísticas gerais")
        print("2. Consultar por tipo de processo")
        print("3. Consultar por empresa")
        print("4. Apenas desdobramentos respondidos")
        print("5. Apenas desdobramentos pendentes")
        print("6. Buscar por palavra-chave (ex: DIRB, REINF, Faturamento)")
        print("7. Consulta personalizada")
        print("0. Sair")
        
        opcao = input("\n➡️  Digite o número da opção: ").strip()
        
        if opcao == "0":
            print("\n👋 Até logo!\n")
            break
        
        elif opcao == "1":
            estatisticas_desdobramentos()
        
        elif opcao == "2":
            print("\nTipos disponíveis:")
            print("  - SimplesNacional")
            print("  - LucroPresumido_Servicos")
            print("  - LucroPresumido_Comercio")
            print("  - LucroReal_Comercio")
            print("  - LucroReal_Servicos")
            tipo = input("\n➡️  Digite o tipo: ").strip()
            consultar_desdobramentos(tipo_processo=tipo)
        
        elif opcao == "3":
            empresa = input("\n➡️  Digite parte do nome da empresa: ").strip()
            consultar_desdobramentos(empresa=empresa)
        
        elif opcao == "4":
            consultar_desdobramentos(apenas_respondidos=True)
        
        elif opcao == "5":
            consultar_desdobramentos(apenas_pendentes=True)
        
        elif opcao == "6":
            palavra = input("\n➡️  Digite a palavra-chave (ex: DIRB, REINF): ").strip()
            consultar_por_pergunta(palavra)
        
        elif opcao == "7":
            print("\n=== CONSULTA PERSONALIZADA ===")
            tipo = input("Tipo de processo (Enter para todos): ").strip() or None
            empresa = input("Nome da empresa (Enter para todas): ").strip() or None
            
            filtro = input("Filtrar por status? (1=Respondidos, 2=Pendentes, Enter=Todos): ").strip()
            apenas_resp = filtro == "1"
            apenas_pend = filtro == "2"
            
            consultar_desdobramentos(
                tipo_processo=tipo,
                empresa=empresa,
                apenas_respondidos=apenas_resp,
                apenas_pendentes=apenas_pend
            )
        
        else:
            print("\n❌ Opção inválida!")
        
        input("\n⏸️  Pressione Enter para continuar...")
