"""
SINCRONIZADOR PRINCIPAL - Versão Profissional
Adaptação completa do fluxo: API → Banco de Dados SQLite

Substitui o fluxo antigo: API → Excel
Novo fluxo: API → SQLite (site faz download Excel sob demanda)
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple
import logging

# Adicionar paths
sys.path.insert(0, str(Path(__file__).parent))
backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

# Imports dos scripts existentes
from api_client import AcessoriasAPI
from dotenv import load_dotenv
import os

# Imports do backend
from app.database import SessionLocal, Base, engine
from app.models import Empresa, Processo, Passo, Desdobramento, Sincronizacao

# Criar tabelas
Base.metadata.create_all(bind=engine)

# Configurar logging
def configurar_logging():
    log_dir = Path('../logs')
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f'sync_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

# Tipos de processos (mesmos do script original)
TIPOS_PROCESSOS = [
    {
        'nome': 'Simples Nacional — Mensal',
        'codigo': 'SimplesNacional',
        'descricao': 'Processos de empresas do Simples Nacional'
    },
    {
        'nome': 'Lucro Presumido - Serviços',
        'codigo': 'LucroPresumido_Servicos',
        'descricao': 'Processos de empresas do Lucro Presumido (Serviços)'
    },
    {
        'nome': 'Lucro Presumido - Comércio, Industria e Serviços',
        'codigo': 'LucroPresumido_Comercio',
        'descricao': 'Processos de empresas do Lucro Presumido (Comércio/Indústria)'
    },
    {
        'nome': 'Lucro Real - Comércio e Industria',
        'codigo': 'LucroReal_Comercio',
        'descricao': 'Processos de empresas do Lucro Real (Comércio/Indústria)'
    },
    {
        'nome': 'Lucro Real - Serviços',
        'codigo': 'LucroReal_Servicos',
        'descricao': 'Processos de empresas do Lucro Real (Serviços)'
    }
]

class SincronizadorProfissional:
    """
    Sincronizador completo: API Acessórias → SQLite
    """
    
    def __init__(self):
        # Carregar .env
        load_dotenv()
        
        # API Client (passar token do .env)
        api_token = os.getenv('ACESSORIAS_API_TOKEN', '7f8129c6ac10075cb95cc08c81a6f219')
        self.api = AcessoriasAPI(api_token=api_token)
        
        # Database session
        self.db = SessionLocal()
        
        # Logger
        self.logger = configurar_logging()
        
        # Estatísticas
        self.stats = {
            'empresas_novas': 0,
            'empresas_atualizadas': 0,
            'processos_novos': 0,
            'processos_atualizados': 0,
            'passos_total': 0,
            'desdobramentos_total': 0,
            'processos_por_regime': {}
        }
        
        # Cache de empresas (evita queries repetidas)
        self.empresas_cache = {}
    
    def buscar_processos_por_tipo(self, tipo: Dict) -> List[Dict]:
        """
        Busca processos de um tipo específico da API
        Usa a mesma lógica do script original
        """
        nome = tipo['nome']
        
        print(f"\n{'='*70}")
        print(f"BUSCANDO: {nome}")
        print(f"{'='*70}")
        self.logger.info(f"\n{'='*70}")
        self.logger.info(f"BUSCANDO: {nome}")
        self.logger.info(f"{'='*70}")
        
        # Buscar processos em andamento
        print(f"🔍 Processos EM ANDAMENTO...")
        self.logger.info(f"🔍 Processos EM ANDAMENTO...")
        processos_andamento = self.api.get_all_processes_paginated(
            proc_status='A',
            proc_nome=nome,
            with_details=True
        )
        print(f"   ✓ {len(processos_andamento)} encontrados")
        self.logger.info(f"   ✓ {len(processos_andamento)} encontrados")
        
        # Buscar processos concluídos
        print(f"🔍 Processos CONCLUÍDOS...")
        self.logger.info(f"🔍 Processos CONCLUÍDOS...")
        processos_concluidos = self.api.get_all_processes_paginated(
            proc_status='C',
            proc_nome=nome,
            with_details=True
        )
        print(f"   ✓ {len(processos_concluidos)} encontrados")
        self.logger.info(f"   ✓ {len(processos_concluidos)} encontrados")
        
        # Combinar
        todos_processos = processos_andamento + processos_concluidos
        
        # Stats
        total = len(todos_processos)
        andamento = len(processos_andamento)
        concluidos = len(processos_concluidos)
        taxa = (concluidos / total * 100) if total > 0 else 0
        
        print(f"\n📊 RESUMO:")
        print(f"   Total: {total}")
        print(f"   Em andamento: {andamento}")
        print(f"   Concluídos: {concluidos}")
        print(f"   Taxa: {taxa:.1f}%")
        self.logger.info(f"\n📊 RESUMO:")
        self.logger.info(f"   Total: {total}")
        self.logger.info(f"   Em andamento: {andamento}")
        self.logger.info(f"   Concluídos: {concluidos}")
        self.logger.info(f"   Taxa: {taxa:.1f}%")
        
        self.stats['processos_por_regime'][tipo['codigo']] = {
            'total': total,
            'andamento': andamento,
            'concluidos': concluidos,
            'taxa_conclusao': taxa
        }
        
        return todos_processos
    
    def salvar_no_banco(self, processos: List[Dict], regime: str):
        """
        Salva processos no banco de dados
        """
        if not processos:
            print(f"⚠️ Nenhum processo para salvar ({regime})")
            self.logger.warning(f"⚠️ Nenhum processo para salvar ({regime})")
            return
        
        print(f"\n💾 Salvando {len(processos)} processos no banco...")
        self.logger.info(f"\n💾 Salvando {len(processos)} processos no banco...")
        
        novos = 0
        atualizados = 0
        
        for proc_data in processos:
            try:
                # 1. Obter empresa
                empresa = self._obter_ou_criar_empresa(proc_data, regime)
                
                # 2. Verificar se processo existe
                proc_id = proc_data.get('ProcID')
                if not proc_id:
                    self.logger.warning(f"   ⚠️ Processo sem ID, pulando...")
                    continue
                
                processo_existente = self.db.query(Processo).filter(
                    Processo.proc_id == proc_id
                ).first()
                
                # 3. Criar ou atualizar processo
                if processo_existente:
                    processo = processo_existente
                    atualizados += 1
                else:
                    processo = Processo()
                    novos += 1
                
                # Atualizar campos
                processo.proc_id = proc_id
                processo.empresa_id = empresa.id
                processo.nome = proc_data.get('ProcNome', 'Sem nome')
                processo.competencia = self._extrair_competencia(proc_data)
                processo.status = self._determinar_status(proc_data)
                processo.porcentagem_conclusao = self._calcular_porcentagem(proc_data)
                processo.regime_tributario = regime
                
                # Contar passos
                passos_lista = proc_data.get('ProcPassos', [])
                processo.total_passos = len(passos_lista)
                processo.passos_concluidos = sum(
                    1 for p in passos_lista 
                    if p.get('PassoConcluido')
                )
                
                if not processo_existente:
                    self.db.add(processo)
                
                self.db.flush()
                
                # 4. Limpar passos/desdobramentos antigos se for update
                if processo_existente:
                    self.db.query(Passo).filter(
                        Passo.processo_id == processo.id
                    ).delete()
                    self.db.query(Desdobramento).filter(
                        Desdobramento.processo_id == processo.id
                    ).delete()
                
                # 5. Salvar passos
                for idx, passo_data in enumerate(passos_lista):
                    passo = Passo(
                        processo_id=processo.id,
                        passo_id=passo_data.get('PassoID', idx),
                        ordem=passo_data.get('PassoOrdem', idx),
                        nome=passo_data.get('PassoNome', 'Sem nome'),
                        descricao=passo_data.get('PassoDescricao', ''),
                        concluido=bool(passo_data.get('PassoConcluido', False))
                    )
                    self.db.add(passo)
                    self.stats['passos_total'] += 1
                    
                    # 6. Salvar desdobramentos do passo
                    desdobr_lista = passo_data.get('PassoDesdobramentos', [])
                    for desdobr_idx, desdobr_data in enumerate(desdobr_lista):
                        desdobr = Desdobramento(
                            processo_id=processo.id,
                            passo_id=passo.passo_id,
                            desdobramento_id=desdobr_data.get('DesdobramentoID', desdobr_idx),
                            pergunta=desdobr_data.get('DesdobramentoPergunta', ''),
                            resposta=desdobr_data.get('DesdobramentoResposta'),
                            tipo='BINARIO',
                            ordem=desdobr_idx,
                            respondido=bool(desdobr_data.get('DesdobramentoResposta'))
                        )
                        self.db.add(desdobr)
                        self.stats['desdobramentos_total'] += 1
                
            except Exception as e:
                self.logger.error(f"   ❌ Erro ao salvar processo {proc_id}: {e}")
                continue
        
        # Commit tudo
        self.db.commit()
        
        print(f"   ✓ Novos: {novos}, Atualizados: {atualizados}")
        self.logger.info(f"   ✓ Novos: {novos}, Atualizados: {atualizados}")
        
        self.stats['processos_novos'] += novos
        self.stats['processos_atualizados'] += atualizados
    
    def _obter_ou_criar_empresa(self, proc_data: Dict, regime: str) -> Empresa:
        """Busca ou cria empresa (com cache)"""
        empresa_nome = proc_data.get('EmpNome', 'Empresa Desconhecida')
        
        # Criar código único
        codigo = f"{regime}_{empresa_nome[:50]}"
        
        # Verificar cache
        if codigo in self.empresas_cache:
            return self.empresas_cache[codigo]
        
        # Buscar no banco
        empresa = self.db.query(Empresa).filter(
            Empresa.codigo == codigo
        ).first()
        
        if not empresa:
            empresa = Empresa(
                codigo=codigo,
                nome=empresa_nome,
                cnpj=proc_data.get('EmpCNPJ'),
                regime_tributario=regime,
                ativa=True
            )
            self.db.add(empresa)
            self.db.flush()
            self.stats['empresas_novas'] += 1
        
        # Cachear
        self.empresas_cache[codigo] = empresa
        
        return empresa
    
    def _extrair_competencia(self, proc_data: Dict) -> str:
        """Extrai competência do processo"""
        # Tentar diferentes campos
        comp = proc_data.get('ProcCompetencia')
        if comp:
            return comp
        
        # Tentar extrair de datas
        data_inicio = proc_data.get('ProcDataInicio', '')
        if data_inicio and '/' in data_inicio:
            partes = data_inicio.split('/')
            if len(partes) >= 3:
                mes = partes[1]
                ano = partes[2]
                return f"{mes}/{ano}"
        
        return "10/2025"  # Default
    
    def _determinar_status(self, proc_data: Dict) -> str:
        """Determina status do processo"""
        if proc_data.get('ProcConcluido'):
            return "CONCLUIDO"
        elif proc_data.get('ProcAndamento'):
            return "EM_ANDAMENTO"
        else:
            return "PENDENTE"
    
    def _calcular_porcentagem(self, proc_data: Dict) -> float:
        """Calcula porcentagem de conclusão"""
        passos = proc_data.get('ProcPassos', [])
        if not passos:
            return 0.0
        
        concluidos = sum(1 for p in passos if p.get('PassoConcluido'))
        return round((concluidos / len(passos)) * 100, 2)
    
    def executar_sincronizacao_completa(self):
        """
        Executa sincronização completa de todos os regimes
        """
        inicio = datetime.now()
        
        print("\n" + "="*70)
        print(" 🚀 SINCRONIZAÇÃO COMPLETA - API → BANCO DE DADOS")
        print("="*70)
        self.logger.info("\n" + "="*70)
        self.logger.info(" 🚀 SINCRONIZAÇÃO COMPLETA - API → BANCO DE DADOS")
        self.logger.info("="*70)
        
        # Registrar início
        sync_log = Sincronizacao(
            tipo="FULL",
            competencia="10/2025",
            status="INICIADA"
        )
        self.db.add(sync_log)
        self.db.commit()
        
        try:
            # Processar cada regime
            for tipo in TIPOS_PROCESSOS:
                # 1. Buscar da API
                processos = self.buscar_processos_por_tipo(tipo)
                
                # 2. Salvar no banco
                self.salvar_no_banco(processos, tipo['codigo'])
            
            # Concluir sincronização
            tempo_total = (datetime.now() - inicio).seconds
            
            sync_log.status = "CONCLUIDA"
            sync_log.total_processos = self.stats['processos_novos'] + self.stats['processos_atualizados']
            sync_log.processos_novos = self.stats['processos_novos']
            sync_log.processos_atualizados = self.stats['processos_atualizados']
            sync_log.tempo_execucao = tempo_total
            sync_log.concluida_em = datetime.now()
            self.db.commit()
            
            # Mostrar resumo
            self._mostrar_resumo_final(tempo_total)
            
        except Exception as e:
            self.logger.error(f"\n❌ ERRO FATAL: {e}")
            import traceback
            traceback.print_exc()
            
            sync_log.status = "ERRO"
            sync_log.mensagem_erro = str(e)
            sync_log.concluida_em = datetime.now()
            self.db.commit()
        
        finally:
            self.db.close()
    
    def _mostrar_resumo_final(self, tempo_total: int):
        """Mostra resumo detalhado da sincronização"""
        print("\n" + "="*70)
        print(" ✅ SINCRONIZAÇÃO CONCLUÍDA!")
        print("="*70)
        print(f" ⏱️  Tempo total: {tempo_total}s")
        self.logger.info("\n" + "="*70)
        self.logger.info(" ✅ SINCRONIZAÇÃO CONCLUÍDA!")
        self.logger.info("="*70)
        self.logger.info(f" ⏱️  Tempo total: {tempo_total}s")
        
        print(f"\n📊 ESTATÍSTICAS GERAIS:")
        print(f"   • Empresas novas: {self.stats['empresas_novas']}")
        print(f"   • Processos novos: {self.stats['processos_novos']}")
        print(f"   • Processos atualizados: {self.stats['processos_atualizados']}")
        print(f"   • Total de passos: {self.stats['passos_total']}")
        print(f"   • Total de desdobramentos: {self.stats['desdobramentos_total']}")
        self.logger.info(f"\n📊 ESTATÍSTICAS GERAIS:")
        self.logger.info(f"   • Empresas novas: {self.stats['empresas_novas']}")
        self.logger.info(f"   • Processos novos: {self.stats['processos_novos']}")
        self.logger.info(f"   • Processos atualizados: {self.stats['processos_atualizados']}")
        self.logger.info(f"   • Total de passos: {self.stats['passos_total']}")
        self.logger.info(f"   • Total de desdobramentos: {self.stats['desdobramentos_total']}")
        
        print(f"\n📋 POR REGIME:")
        self.logger.info(f"\n📋 POR REGIME:")
        for regime, dados in self.stats['processos_por_regime'].items():
            print(f"   • {regime}: {dados['total']} processos ({dados['taxa_conclusao']:.1f}% concluídos)")
            self.logger.info(f"   • {regime}: {dados['total']} processos ({dados['taxa_conclusao']:.1f}% concluídos)")
        
        # Verificar totais no banco
        total_empresas = self.db.query(Empresa).count()
        total_processos = self.db.query(Processo).count()
        total_passos = self.db.query(Passo).count()
        total_desdobr = self.db.query(Desdobramento).count()
        
        print(f"\n💾 TOTAIS NO BANCO:")
        print(f"   • Empresas: {total_empresas}")
        print(f"   • Processos: {total_processos}")
        print(f"   • Passos: {total_passos}")
        print(f"   • Desdobramentos: {total_desdobr}")
        print("="*70 + "\n")
        self.logger.info(f"\n💾 TOTAIS NO BANCO:")
        self.logger.info(f"   • Empresas: {total_empresas}")
        self.logger.info(f"   • Processos: {total_processos}")
        self.logger.info(f"   • Passos: {total_passos}")
        self.logger.info(f"   • Desdobramentos: {total_desdobr}")
        self.logger.info("="*70 + "\n")

if __name__ == "__main__":
    sincronizador = SincronizadorProfissional()
    sincronizador.executar_sincronizacao_completa()
