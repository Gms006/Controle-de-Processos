"""
Script para popular banco de dados a partir dos dados existentes (Excel)
Usar apenas na primeira vez ou para rebuild
"""
import sys
from pathlib import Path
import pandas as pd
from datetime import datetime

# Adicionar backend ao path
backend_dir = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_dir))

from app.database import SessionLocal, engine, Base
from app.models import Empresa, Processo, Passo, Desdobramento, Sincronizacao

def popular_banco_de_excel():
    """
    Popula banco SQLite a partir dos arquivos Excel existentes
    """
    print("\n" + "="*70)
    print(" 📊 POPULANDO BANCO DE DADOS A PARTIR DOS EXCEL")
    print("="*70)
    
    # Criar tabelas
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas no SQLite")
    
    db = SessionLocal()
    
    # Registrar sincronização
    sync = Sincronizacao(
        tipo="FULL",
        competencia="10/2025",
        status="INICIADA"
    )
    db.add(sync)
    db.commit()
    
    start_time = datetime.now()
    
    try:
        # Buscar arquivos Excel - pegar apenas o mais recente de cada regime
        planilhas_dir = Path(__file__).parent.parent / 'output' / 'planilhas'
        all_files = list(planilhas_dir.glob('*DadosBrutos*.xlsx'))
        
        # Agrupar por regime e pegar mais recente
        regimes_files = {}
        for f in all_files:
            if 'SimplesNacional' in f.name:
                regime_key = 'SimplesNacional'
            elif 'LucroPresumido_Comercio' in f.name:
                regime_key = 'LucroPresumido_Comercio'
            elif 'LucroPresumido_Servicos' in f.name:
                regime_key = 'LucroPresumido_Servicos'
            elif 'LucroReal_Comercio' in f.name:
                regime_key = 'LucroReal_Comercio'
            elif 'LucroReal_Servicos' in f.name:
                regime_key = 'LucroReal_Servicos'
            else:
                continue
            
            # Pegar mais recente
            if regime_key not in regimes_files or f.stat().st_mtime > regimes_files[regime_key].stat().st_mtime:
                regimes_files[regime_key] = f
        
        excel_files = list(regimes_files.values())
        
        print(f"\n📁 Processando {len(excel_files)} regimes (mais recente de cada):")
        for f in excel_files:
            print(f"   - {f.name}")
        
        total_processos = 0
        total_passos = 0
        total_desdobramentos = 0
        empresas_criadas = {}
        processos_criados = set()  # Para evitar duplicados
        
        for excel_file in excel_files:
            print(f"\n🔄 Processando {excel_file.name}...")
            
            # Identificar regime pelo nome do arquivo
            if 'SimplesNacional' in excel_file.name:
                regime = 'SimplesNacional'
            elif 'LucroPresumido' in excel_file.name:
                regime = 'LucroPresumido'
            elif 'LucroReal' in excel_file.name:
                regime = 'LucroReal'
            else:
                regime = 'Desconhecido'
            
            # Ler abas
            df_geral = pd.read_excel(excel_file, sheet_name='PROCESSOS_GERAL')
            
            # Verificar se tem as outras abas (alguns Excel podem não ter)
            try:
                df_passos = pd.read_excel(excel_file, sheet_name='PROCESSOS_PASSOS')
            except:
                df_passos = pd.DataFrame()
            
            try:
                df_desdobramentos = pd.read_excel(excel_file, sheet_name='PROCESSOS_DESDOBRAMENTOS')
            except:
                df_desdobramentos = pd.DataFrame()
            
            print(f"   📋 {len(df_geral)} processos")
            print(f"   📝 {len(df_passos)} passos")
            print(f"   ❓ {len(df_desdobramentos)} desdobramentos")
            
            # Processar cada processo
            for _, row in df_geral.iterrows():
                # 1. Criar/buscar empresa
                empresa_nome = str(row.get('EMPRESA', 'Desconhecida'))
                # Usar combinação regime + nome para código único
                empresa_codigo = f"{regime}_{empresa_nome[:20]}".replace(' ', '_')
                
                if empresa_codigo not in empresas_criadas:
                    empresa = Empresa(
                        codigo=empresa_codigo,
                        nome=empresa_nome,
                        regime_tributario=regime,
                        ativa=True
                    )
                    db.add(empresa)
                    db.flush()
                    empresas_criadas[empresa_codigo] = empresa.id
                
                empresa_id = empresas_criadas[empresa_codigo]
                
                # 2. Criar processo
                proc_id = int(row['PROC_ID'])
                
                # Pular se já existe
                if proc_id in processos_criados:
                    continue
                
                processos_criados.add(proc_id)
                
                processo = Processo(
                    proc_id=proc_id,
                    empresa_id=empresa_id,
                    nome=str(row.get('NOME_PROCESSO', f'Processo {proc_id}')),
                    competencia='10/2025',
                    status=str(row.get('STATUS', 'PENDENTE')),
                    porcentagem_conclusao=float(row.get('PORCENTAGEM', 0)),
                    total_passos=int(row.get('TOTAL_PASSOS', 0)),
                    passos_concluidos=int(row.get('PASSOS_CONCLUIDOS', 0)),
                    dias_corridos=int(row.get('DIAS_CORRIDOS', 0)) if pd.notna(row.get('DIAS_CORRIDOS')) else None,
                    regime_tributario=regime,
                    hash_snapshot='initial'
                )
                db.add(processo)
                db.flush()
                total_processos += 1
                
                # 3. Adicionar passos
                if not df_passos.empty and 'PROC_ID' in df_passos.columns:
                    passos_processo = df_passos[df_passos['PROC_ID'] == proc_id]
                    for idx, passo_row in passos_processo.iterrows():
                        passo = Passo(
                            passo_id=int(passo_row.get('PASSO_ID', idx)),
                            processo_id=processo.id,
                            ordem=int(passo_row.get('ORDEM', idx)),
                            nome=str(passo_row.get('NOME', 'Passo sem nome')),
                            descricao=str(passo_row.get('DESCRICAO', '')) if pd.notna(passo_row.get('DESCRICAO')) else None,
                            concluido=bool(passo_row.get('CONCLUIDO', False))
                        )
                        db.add(passo)
                        total_passos += 1
                
                # 4. Adicionar desdobramentos
                if not df_desdobramentos.empty and 'PROC_ID' in df_desdobramentos.columns:
                    desdobr_processo = df_desdobramentos[df_desdobramentos['PROC_ID'] == proc_id]
                    for idx, desdobr_row in desdobr_processo.iterrows():
                        desdobr = Desdobramento(
                            desdobramento_id=int(desdobr_row.get('DESDOBR_ID', idx)),
                            processo_id=processo.id,
                            passo_id=int(desdobr_row.get('PASSO_ID', 0)) if pd.notna(desdobr_row.get('PASSO_ID')) else None,
                            pergunta=str(desdobr_row.get('PERGUNTA', 'Pergunta não especificada')),
                            resposta=str(desdobr_row.get('RESPOSTA', '')) if pd.notna(desdobr_row.get('RESPOSTA')) else None,
                            tipo=str(desdobr_row.get('TIPO', 'TEXTO')),
                            ordem=int(desdobr_row.get('ORDEM', idx)),
                            respondido=bool(desdobr_row.get('RESPONDIDO', False))
                        )
                        db.add(desdobr)
                        total_desdobramentos += 1
            
            db.commit()
            print(f"   ✅ Processado com sucesso!")
        
        # Finalizar sincronização
        tempo_exec = (datetime.now() - start_time).seconds
        sync.status = "CONCLUIDA"
        sync.total_processos = total_processos
        sync.processos_novos = total_processos
        sync.processos_atualizados = 0
        sync.tempo_execucao = tempo_exec
        sync.concluida_em = datetime.now()
        db.commit()
        
        print("\n" + "="*70)
        print(" ✅ BANCO DE DADOS POPULADO COM SUCESSO!")
        print("="*70)
        print(f" 🏢 Empresas: {len(empresas_criadas)}")
        print(f" 📋 Processos: {total_processos}")
        print(f" 📝 Passos: {total_passos}")
        print(f" ❓ Desdobramentos: {total_desdobramentos}")
        print(f" ⏱️  Tempo: {tempo_exec}s")
        print("="*70)
        
        # Validar dados
        print("\n🔍 Validação:")
        print(f"   Empresas no DB: {db.query(Empresa).count()}")
        print(f"   Processos no DB: {db.query(Processo).count()}")
        print(f"   Passos no DB: {db.query(Passo).count()}")
        print(f"   Desdobramentos no DB: {db.query(Desdobramento).count()}")
        
    except Exception as e:
        sync.status = "ERRO"
        sync.mensagem_erro = str(e)
        sync.concluida_em = datetime.now()
        db.commit()
        print(f"\n❌ ERRO: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    popular_banco_de_excel()
