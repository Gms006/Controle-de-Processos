"""
SINCRONIZAÇÃO FINAL - APENAS SIMPLES NACIONAL
Script simplificado para completar a sincronização
"""

import sys
from pathlib import Path

# Paths
sys.path.insert(0, str(Path(__file__).parent))
backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

from api_client import AcessoriasAPI
from dotenv import load_dotenv
import os
from app.database import SessionLocal
from app.models import Empresa, Processo, Passo, Desdobramento

load_dotenv()

def main():
    print("=" * 80)
    print("SINCRONIZANDO: SIMPLES NACIONAL")
    print("=" * 80)
    
    # API
    api_token = os.getenv('ACESSORIAS_API_TOKEN', '7f8129c6ac10075cb95cc08c81a6f219')
    api = AcessoriasAPI(api_token=api_token)
    
    # Database
    db = SessionLocal()
    
    try:
        # Buscar processos do Simples Nacional
        nome = 'Simples Nacional — Mensal'
        codigo_regime = 'SimplesNacional'
        
        print(f"\n🔍 Buscando processos: {nome}")
        print(f"   Aguarde, este processo pode demorar...")
        print()
        
        # Em andamento
        print(f"⏳ Buscando processos EM ANDAMENTO...")
        andamento = api.get_all_processes_paginated(
            proc_status='A',
            proc_nome=nome,
            with_details=True
        )
        print(f"✅ {len(andamento)} encontrados")
        
        # Concluídos  
        print(f"⏳ Buscando processos CONCLUÍDOS...")
        concluidos = api.get_all_processes_paginated(
            proc_status='C',
            proc_nome=nome,
            with_details=True
        )
        print(f"✅ {len(concluidos)} encontrados")
        
        todos = andamento + concluidos
        print(f"\n📊 TOTAL: {len(todos)} processos")
        
        if not todos:
            print("⚠️  Nenhum processo encontrado!")
            return
        
        # Salvar no banco
        print(f"\n💾 Salvando no banco de dados...")
        empresas_cache = {}
        novos = 0
        atualizados = 0
        
        for idx, proc_data in enumerate(todos, 1):
            try:
                # Progress
                if idx % 10 == 0 or idx == 1:
                    print(f"   Processando {idx}/{len(todos)}...")
                
                # Empresa
                emp_nome = proc_data.get('EmpNome', 'Desconhecida')
                emp_cnpj = proc_data.get('EmpCNPJ', '')
                cache_key = f"SimplesNacional_{emp_nome[:50]}"
                
                if cache_key not in empresas_cache:
                    empresa = db.query(Empresa).filter(Empresa.codigo == cache_key).first()
                    if not empresa:
                        empresa = Empresa(
                            codigo=cache_key,
                            nome=emp_nome[:200],
                            cnpj=emp_cnpj[:18],
                            regime_tributario='SimplesNacional',
                            ativa=True
                        )
                        db.add(empresa)
                        db.flush()
                    empresas_cache[cache_key] = empresa
                else:
                    empresa = empresas_cache[cache_key]
                
                # Processo
                proc_id = proc_data.get('ProcID')
                passos_data = proc_data.get('ProcPassos', [])
                total_passos = len(passos_data)
                passos_concluidos = sum(1 for p in passos_data if p.get('PassoConcluido'))
                porcentagem = (passos_concluidos / total_passos * 100) if total_passos > 0 else 0
                
                status = 'CONCLUIDO' if proc_data.get('ProcConcluido') else \
                         'EM_ANDAMENTO' if proc_data.get('ProcAndamento') else 'PENDENTE'
                
                processo = db.query(Processo).filter(Processo.proc_id == proc_id).first()
                
                if not processo:
                    processo = Processo(
                        proc_id=proc_id,
                        empresa_id=empresa.id,
                        nome=proc_data.get('ProcNome', 'Processo')[:200],
                        competencia=proc_data.get('ProcCompetencia', '10/2025')[:7],
                        status=status,
                        porcentagem_conclusao=porcentagem,
                        total_passos=total_passos,
                        passos_concluidos=passos_concluidos,
                        regime_tributario='SimplesNacional'
                    )
                    db.add(processo)
                    db.flush()
                    novos += 1
                else:
                    processo.porcentagem_conclusao = porcentagem
                    processo.status = status
                    processo.passos_concluidos = passos_concluidos
                    atualizados += 1
                
                # Passos
                for passo_data in passos_data:
                    passo_id = passo_data.get('PassoID')
                    passo = db.query(Passo).filter(
                        Passo.passo_id == passo_id,
                        Passo.processo_id == processo.id
                    ).first()
                    
                    if not passo:
                        passo = Passo(
                            passo_id=passo_id,
                            processo_id=processo.id,
                            ordem=passo_data.get('PassoOrdem', 0),
                            nome=passo_data.get('PassoNome', '')[:200],
                            concluido=passo_data.get('PassoConcluido', False)
                        )
                        db.add(passo)
                        db.flush()
                    
                    # Desdobramentos
                    for desd_data in passo_data.get('PassoDesdobramentos', []):
                        desd_id = desd_data.get('DesdobramentoID')
                        desd = db.query(Desdobramento).filter(
                            Desdobramento.desdobramento_id == desd_id,
                            Desdobramento.processo_id == processo.id
                        ).first()
                        
                        if not desd:
                            desd = Desdobramento(
                                desdobramento_id=desd_id,
                                processo_id=processo.id,
                                passo_id=passo.passo_id,
                                pergunta=desd_data.get('DesdobramentoPergunta', '')[:500],
                                resposta=desd_data.get('DesdobramentoResposta', ''),
                                respondido=bool(desd_data.get('DesdobramentoResposta'))
                            )
                            db.add(desd)
                
                # Commit a cada 10
                if idx % 10 == 0:
                    db.commit()
            
            except Exception as e:
                print(f"   ⚠️  Erro no processo {proc_id}: {e}")
                continue
        
        # Commit final
        db.commit()
        
        print(f"\n✅ CONCLUÍDO!")
        print(f"   Novos: {novos}")
        print(f"   Atualizados: {atualizados}")
        print("=" * 80)
        
    except KeyboardInterrupt:
        print(f"\n⚠️  Sincronização interrompida pelo usuário")
        db.rollback()
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    main()
