"""
Script de sincronização SIMPLIFICADO e ROBUSTO
Usa o mesmo fluxo que já funcionou para LucroPresumido e LucroReal
"""

import sys
from pathlib import Path

# Adicionar paths
sys.path.insert(0, str(Path(__file__).parent))
backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

from api_client import AcessoriasAPI
from dotenv import load_dotenv
import os
from datetime import datetime
from app.database import SessionLocal, Base, engine
from app.models import Empresa, Processo, Passo, Desdobramento, Sincronizacao

# Criar tabelas
Base.metadata.create_all(bind=engine)

# Carregar .env
load_dotenv()

# Tipos de processos
TIPOS_PROCESSOS = [
    {
        'nome': 'Simples Nacional — Mensal',
        'codigo': 'SimplesNacional',
    },
    {
        'nome': 'Lucro Presumido - Serviços',
        'codigo': 'LucroPresumido_Servicos',
    },
    {
        'nome': 'Lucro Presumido - Comércio, Industria e Serviços',
        'codigo': 'LucroPresumido_Comercio',
    },
    {
        'nome': 'Lucro Real - Comércio e Industria',
        'codigo': 'LucroReal_Comercio',
    },
    {
        'nome': 'Lucro Real - Serviços',
        'codigo': 'LucroReal_Servicos',
    }
]

def verificar_regimes_pendentes(db):
    """Verifica quais regimes já foram sincronizados"""
    result = db.execute(
        "SELECT DISTINCT regime_tributario FROM empresas"
    )
    sincronizados = [row[0] for row in result.fetchall()]
    
    pendentes = []
    for tipo in TIPOS_PROCESSOS:
        # Verificar se regime já está no banco
        # SimplesNacional → SimplesNacional
        # LucroPresumido_Servicos → LucroPresumido
        # LucroReal_Comercio → LucroReal
        regime_base = tipo['codigo'].split('_')[0]
        
        if regime_base not in sincronizados:
            pendentes.append(tipo)
    
    return pendentes, sincronizados

def main():
    db = SessionLocal()
    
    try:
        print("=" * 80)
        print("SINCRONIZAÇÃO INTELIGENTE - PROCESSOS CONTÁBEIS")
        print("=" * 80)
        
        # Verificar regimes pendentes
        pendentes, sincronizados = verificar_regimes_pendentes(db)
        
        print(f"\n📊 STATUS ATUAL:")
        print(f"   Regimes sincronizados: {', '.join(sincronizados) if sincronizados else 'Nenhum'}")
        print(f"   Regimes pendentes: {len(pendentes)}")
        print()
        
        if not pendentes:
            print("✅ Todos os regimes já foram sincronizados!")
            print("\nPara ressincronizar, delete o banco de dados:")
            print("   rm database.db")
            return
        
        # API Client
        api_token = os.getenv('ACESSORIAS_API_TOKEN', '7f8129c6ac10075cb95cc08c81a6f219')
        api = AcessoriasAPI(api_token=api_token)
        
        # Cache de empresas para performance
        empresas_cache = {}
        
        # Processar cada regime pendente
        for tipo in pendentes:
            print(f"\n{'='*80}")
            print(f"📋 REGIME: {tipo['nome']}")
            print(f"   Código: {tipo['codigo']}")
            print(f"{'='*80}")
            
            # Buscar processos
            print(f"\n🔍 Buscando processos...")
            nome = tipo['nome']
            
            # Em andamento
            print(f"   ⏳ Status: EM ANDAMENTO...")
            andamento = api.get_all_processes_paginated(
                proc_status='A',
                proc_nome=nome,
                with_details=True
            )
            print(f"   ✅ {len(andamento)} processos em andamento")
            
            # Concluídos
            print(f"   ⏳ Status: CONCLUÍDOS...")
            concluidos = api.get_all_processes_paginated(
                proc_status='C',
                proc_nome=nome,
                with_details=True
            )
            print(f"   ✅ {len(concluidos)} processos concluídos")
            
            todos = andamento + concluidos
            print(f"\n📊 Total: {len(todos)} processos")
            
            if not todos:
                print(f"   ⚠️  Nenhum processo encontrado para {tipo['nome']}")
                continue
            
            # Salvar no banco
            print(f"\n💾 Salvando no banco de dados...")
            novos = 0
            atualizados = 0
            
            for idx, proc_data in enumerate(todos, 1):
                if idx % 10 == 0:
                    print(f"   ⏳ Processando {idx}/{len(todos)}...")
                
                try:
                    # Obter ou criar empresa
                    emp_nome = proc_data.get('EmpNome', 'Empresa Desconhecida')
                    emp_cnpj = proc_data.get('EmpCNPJ', '')
                    
                    # Cache key
                    cache_key = f"{tipo['codigo']}_{emp_nome}"
                    
                    if cache_key in empresas_cache:
                        empresa = empresas_cache[cache_key]
                    else:
                        # Buscar ou criar empresa
                        empresa = db.query(Empresa).filter(
                            Empresa.codigo == cache_key
                        ).first()
                        
                        if not empresa:
                            empresa = Empresa(
                                codigo=cache_key,
                                nome=emp_nome[:200],
                                cnpj=emp_cnpj[:18],
                                regime_tributario=tipo['codigo'].split('_')[0],
                                ativa=True
                            )
                            db.add(empresa)
                            db.flush()
                        
                        empresas_cache[cache_key] = empresa
                    
                    # Processo
                    proc_id = proc_data.get('ProcID')
                    processo = db.query(Processo).filter(
                        Processo.proc_id == proc_id
                    ).first()
                    
                    # Calcular porcentagem
                    passos_data = proc_data.get('ProcPassos', [])
                    total_passos = len(passos_data)
                    passos_concluidos = sum(1 for p in passos_data if p.get('PassoConcluido'))
                    porcentagem = (passos_concluidos / total_passos * 100) if total_passos > 0 else 0
                    
                    # Determinar status
                    if proc_data.get('ProcConcluido'):
                        status = 'CONCLUIDO'
                    elif proc_data.get('ProcAndamento'):
                        status = 'EM_ANDAMENTO'
                    else:
                        status = 'PENDENTE'
                    
                    # Extrair competência
                    competencia = proc_data.get('ProcCompetencia', '10/2025')
                    
                    if not processo:
                        # Criar novo processo
                        processo = Processo(
                            proc_id=proc_id,
                            empresa_id=empresa.id,
                            nome=proc_data.get('ProcNome', 'Processo')[:200],
                            competencia=competencia[:7],
                            status=status,
                            porcentagem_conclusao=porcentagem,
                            total_passos=total_passos,
                            passos_concluidos=passos_concluidos,
                            regime_tributario=tipo['codigo'].split('_')[0]
                        )
                        db.add(processo)
                        db.flush()
                        novos += 1
                    else:
                        # Atualizar processo existente
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
                                nome=passo_data.get('PassoNome', 'Passo')[:200],
                                descricao=passo_data.get('PassoDescricao', ''),
                                concluido=passo_data.get('PassoConcluido', False)
                            )
                            db.add(passo)
                            db.flush()
                        
                        # Desdobramentos
                        for desdobramento_data in passo_data.get('PassoDesdobramentos', []):
                            desd_id = desdobramento_data.get('DesdobramentoID')
                            desd = db.query(Desdobramento).filter(
                                Desdobramento.desdobramento_id == desd_id,
                                Desdobramento.processo_id == processo.id
                            ).first()
                            
                            if not desd:
                                desd = Desdobramento(
                                    desdobramento_id=desd_id,
                                    processo_id=processo.id,
                                    passo_id=passo.passo_id,
                                    pergunta=desdobramento_data.get('DesdobramentoPergunta', '')[:500],
                                    resposta=desdobramento_data.get('DesdobramentoResposta', ''),
                                    respondido=bool(desdobramento_data.get('DesdobramentoResposta'))
                                )
                                db.add(desd)
                    
                    # Commit a cada 10 processos
                    if idx % 10 == 0:
                        db.commit()
                
                except Exception as e:
                    print(f"   ⚠️  Erro no processo {proc_id}: {e}")
                    continue
            
            # Commit final
            db.commit()
            
            print(f"\n✅ REGIME CONCLUÍDO!")
            print(f"   🆕 Processos novos: {novos}")
            print(f"   🔄 Processos atualizados: {atualizados}")
        
        print(f"\n{'='*80}")
        print("✅ SINCRONIZAÇÃO COMPLETA!")
        print(f"{'='*80}")
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    main()
