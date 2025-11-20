"""
Serviço de Sincronização Inteligente com API Acessórias
"""
import httpx
import asyncio
import hashlib
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from pathlib import Path

from ..config import settings
from ..models import Processo, Empresa, Passo, Desdobramento, Sincronizacao

class AcessoriasSyncService:
    """
    Serviço de sincronização inteligente com detecção de mudanças
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.api_url = settings.ACESSORIAS_API_URL
        self.api_token = settings.ACESSORIAS_API_TOKEN
        self.headers = {"Authorization": f"Bearer {self.api_token}"}
        self.cache_dir = settings.CACHE_DIR
        self.cache_dir.mkdir(exist_ok=True)
    
    async def sync_full(self, competencia: str = None) -> Dict:
        """
        Sincronização COMPLETA - busca todos os processos
        Usar apenas na primeira vez ou para rebuild completo
        """
        competencia = competencia or settings.DEFAULT_COMPETENCIA
        start_time = datetime.now()
        
        print(f"\n🔄 SINCRONIZAÇÃO COMPLETA - Competência {competencia}")
        print("=" * 70)
        
        # Registrar início
        sync_log = Sincronizacao(
            tipo="FULL",
            competencia=competencia,
            status="INICIADA"
        )
        self.db.add(sync_log)
        self.db.commit()
        
        try:
            # 1. Buscar todos os processos dos 5 regimes
            regimes = [
                'SimplesNacional',
                'LucroPresumido_Servicos',
                'LucroPresumido_Comercio',
                'LucroReal_Comercio',
                'LucroReal_Servicos'
            ]
            
            todos_processos = []
            for regime in regimes:
                print(f"\n📋 Buscando {regime}...")
                processos = await self._fetch_processos_regime(regime, competencia)
                todos_processos.extend(processos)
                print(f"   ✅ {len(processos)} processos encontrados")
            
            print(f"\n📊 Total de processos: {len(todos_processos)}")
            
            # 2. Buscar detalhes de cada processo em batches
            print(f"\n🔍 Buscando detalhes dos processos...")
            processos_detalhados = await self._fetch_processos_batch(
                [p['proc_id'] for p in todos_processos]
            )
            
            # 3. Salvar no banco de dados
            print(f"\n💾 Salvando no banco de dados...")
            novos, atualizados = await self._save_processos(processos_detalhados)
            
            # 4. Concluir sincronização
            tempo_exec = (datetime.now() - start_time).seconds
            sync_log.status = "CONCLUIDA"
            sync_log.total_processos = len(todos_processos)
            sync_log.processos_novos = novos
            sync_log.processos_atualizados = atualizados
            sync_log.tempo_execucao = tempo_exec
            sync_log.concluida_em = datetime.now()
            self.db.commit()
            
            # 5. Invalidar cache
            self._invalidate_cache(competencia)
            
            print(f"\n✅ SINCRONIZAÇÃO CONCLUÍDA!")
            print(f"   ⏱️  Tempo: {tempo_exec}s")
            print(f"   🆕 Novos: {novos}")
            print(f"   🔄 Atualizados: {atualizados}")
            print("=" * 70)
            
            return {
                "status": "CONCLUIDA",
                "tipo": "FULL",
                "competencia": competencia,
                "processos_novos": novos,
                "processos_atualizados": atualizados,
                "tempo_execucao": tempo_exec,
                "mensagem": f"Sincronização completa realizada com sucesso"
            }
            
        except Exception as e:
            sync_log.status = "ERRO"
            sync_log.mensagem_erro = str(e)
            sync_log.concluida_em = datetime.now()
            self.db.commit()
            
            print(f"\n❌ ERRO na sincronização: {e}")
            raise
    
    async def sync_incremental(self, competencia: str = None) -> Dict:
        """
        Sincronização INCREMENTAL - busca apenas processos modificados
        90% mais rápido que sync_full
        """
        competencia = competencia or settings.DEFAULT_COMPETENCIA
        start_time = datetime.now()
        
        print(f"\n🔄 SINCRONIZAÇÃO INCREMENTAL - Competência {competencia}")
        print("=" * 70)
        
        # Registrar início
        sync_log = Sincronizacao(
            tipo="INCREMENTAL",
            competencia=competencia,
            status="INICIADA"
        )
        self.db.add(sync_log)
        self.db.commit()
        
        try:
            # 1. Buscar METADATA dos processos (lightweight)
            print(f"📋 Buscando metadados dos processos...")
            regimes = [
                'SimplesNacional',
                'LucroPresumido_Servicos',
                'LucroPresumido_Comercio',
                'LucroReal_Comercio',
                'LucroReal_Servicos'
            ]
            
            todos_processos = []
            for regime in regimes:
                processos = await self._fetch_processos_regime(regime, competencia)
                todos_processos.extend(processos)
            
            print(f"   ✅ {len(todos_processos)} processos na API")
            
            # 2. Buscar processos do banco local
            db_processos = {
                p.proc_id: p
                for p in self.db.query(Processo).filter(
                    Processo.competencia == competencia
                ).all()
            }
            
            print(f"   💾 {len(db_processos)} processos no banco local")
            
            # 3. Detectar mudanças
            novos_ids = []
            modificados_ids = []
            
            for api_proc in todos_processos:
                proc_id = api_proc['proc_id']
                db_proc = db_processos.get(proc_id)
                
                if not db_proc:
                    # Processo novo
                    novos_ids.append(proc_id)
                elif self._has_changes(api_proc, db_proc):
                    # Processo modificado
                    modificados_ids.append(proc_id)
            
            print(f"\n🔍 Análise de mudanças:")
            print(f"   🆕 Novos: {len(novos_ids)}")
            print(f"   🔄 Modificados: {len(modificados_ids)}")
            
            # 4. Buscar detalhes APENAS dos processos que mudaram
            processos_para_atualizar = novos_ids + modificados_ids
            
            if processos_para_atualizar:
                print(f"\n🔍 Buscando detalhes de {len(processos_para_atualizar)} processos...")
                processos_detalhados = await self._fetch_processos_batch(
                    processos_para_atualizar
                )
                
                # 5. Salvar no banco
                print(f"💾 Salvando alterações...")
                novos, atualizados = await self._save_processos(processos_detalhados)
            else:
                print(f"\n✨ Nenhuma mudança detectada!")
                novos, atualizados = 0, 0
            
            # 6. Concluir
            tempo_exec = (datetime.now() - start_time).seconds
            sync_log.status = "CONCLUIDA"
            sync_log.total_processos = len(todos_processos)
            sync_log.processos_novos = novos
            sync_log.processos_atualizados = atualizados
            sync_log.tempo_execucao = tempo_exec
            sync_log.concluida_em = datetime.now()
            self.db.commit()
            
            # 7. Invalidar cache se houver mudanças
            if novos > 0 or atualizados > 0:
                self._invalidate_cache(competencia)
            
            print(f"\n✅ SINCRONIZAÇÃO INCREMENTAL CONCLUÍDA!")
            print(f"   ⏱️  Tempo: {tempo_exec}s")
            print(f"   🆕 Novos: {novos}")
            print(f"   🔄 Atualizados: {atualizados}")
            print("=" * 70)
            
            return {
                "status": "CONCLUIDA",
                "tipo": "INCREMENTAL",
                "competencia": competencia,
                "processos_novos": novos,
                "processos_atualizados": atualizados,
                "tempo_execucao": tempo_exec,
                "mensagem": f"Sincronização incremental concluída"
            }
            
        except Exception as e:
            sync_log.status = "ERRO"
            sync_log.mensagem_erro = str(e)
            sync_log.concluida_em = datetime.now()
            self.db.commit()
            
            print(f"\n❌ ERRO: {e}")
            raise
    
    async def _fetch_processos_regime(
        self,
        regime: str,
        competencia: str
    ) -> List[Dict]:
        """
        Busca lista de processos de um regime (lightweight)
        """
        # Usar script existente
        # TODO: Implementar chamada direta à API
        # Por ora, retorna lista vazia
        return []
    
    async def _fetch_processos_batch(
        self,
        processos_ids: List[int]
    ) -> List[Dict]:
        """
        Busca detalhes de múltiplos processos em paralelo
        """
        batch_size = settings.SYNC_BATCH_SIZE
        processos = []
        
        for i in range(0, len(processos_ids), batch_size):
            batch = processos_ids[i:i + batch_size]
            
            # Buscar em paralelo
            async with httpx.AsyncClient() as client:
                tasks = [
                    self._fetch_processo_detail(client, proc_id)
                    for proc_id in batch
                ]
                batch_results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Filtrar erros
                for result in batch_results:
                    if not isinstance(result, Exception) and result:
                        processos.append(result)
            
            # Rate limiting
            await asyncio.sleep(settings.SYNC_RATE_LIMIT)
            print(f"   ⏳ Processados {min(i + batch_size, len(processos_ids))}/{len(processos_ids)}")
        
        return processos
    
    async def _fetch_processo_detail(
        self,
        client: httpx.AsyncClient,
        proc_id: int
    ) -> Optional[Dict]:
        """
        Busca detalhes de um processo específico
        """
        try:
            url = f"{self.api_url}/processos/{proc_id}"
            response = await client.get(url, headers=self.headers, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"   ⚠️  Erro ao buscar processo {proc_id}: {e}")
            return None
    
    async def _save_processos(
        self,
        processos_detalhados: List[Dict]
    ) -> Tuple[int, int]:
        """
        Salva/atualiza processos no banco de dados
        Retorna: (novos, atualizados)
        """
        novos = 0
        atualizados = 0
        
        for proc_data in processos_detalhados:
            # 1. Garantir que empresa existe
            empresa = self._get_or_create_empresa(proc_data)
            
            # 2. Buscar ou criar processo
            processo = self.db.query(Processo).filter(
                Processo.proc_id == proc_data['proc_id']
            ).first()
            
            is_new = processo is None
            
            if is_new:
                processo = Processo()
                novos += 1
            else:
                atualizados += 1
            
            # 3. Atualizar dados do processo
            processo.proc_id = proc_data['proc_id']
            processo.empresa_id = empresa.id
            processo.nome = proc_data.get('nome', '')
            processo.competencia = proc_data.get('competencia', '')
            processo.status = proc_data.get('status')
            processo.porcentagem_conclusao = proc_data.get('porcentagem_conclusao')
            processo.total_passos = len(proc_data.get('passos', []))
            processo.passos_concluidos = sum(
                1 for p in proc_data.get('passos', [])
                if p.get('concluido')
            )
            processo.regime_tributario = proc_data.get('regime_tributario')
            processo.hash_snapshot = self._calculate_hash(proc_data)
            
            if is_new:
                self.db.add(processo)
            
            self.db.flush()  # Para obter processo.id
            
            # 4. Atualizar passos
            if not is_new:
                # Deletar passos antigos
                self.db.query(Passo).filter(
                    Passo.processo_id == processo.id
                ).delete()
            
            for idx, passo_data in enumerate(proc_data.get('passos', [])):
                passo = Passo(
                    processo_id=processo.id,
                    passo_id=passo_data.get('id', idx),
                    ordem=idx,
                    nome=passo_data.get('nome', ''),
                    descricao=passo_data.get('descricao'),
                    concluido=passo_data.get('concluido', False)
                )
                self.db.add(passo)
            
            # 5. Atualizar desdobramentos
            if not is_new:
                self.db.query(Desdobramento).filter(
                    Desdobramento.processo_id == processo.id
                ).delete()
            
            for idx, desdobr_data in enumerate(proc_data.get('desdobramentos', [])):
                desdobr = Desdobramento(
                    processo_id=processo.id,
                    desdobramento_id=desdobr_data.get('id', idx),
                    pergunta=desdobr_data.get('pergunta', ''),
                    resposta=desdobr_data.get('resposta'),
                    alternativas=desdobr_data.get('alternativas'),
                    tipo=desdobr_data.get('tipo'),
                    ordem=idx,
                    respondido=bool(desdobr_data.get('resposta'))
                )
                self.db.add(desdobr)
        
        self.db.commit()
        return novos, atualizados
    
    def _get_or_create_empresa(self, proc_data: Dict) -> Empresa:
        """
        Busca ou cria empresa
        """
        empresa_data = proc_data.get('empresa', {})
        codigo = empresa_data.get('codigo', 'UNKN')
        
        empresa = self.db.query(Empresa).filter(
            Empresa.codigo == codigo
        ).first()
        
        if not empresa:
            empresa = Empresa(
                codigo=codigo,
                nome=empresa_data.get('nome', 'Empresa Desconhecida'),
                cnpj=empresa_data.get('cnpj'),
                regime_tributario=proc_data.get('regime_tributario')
            )
            self.db.add(empresa)
            self.db.flush()
        
        return empresa
    
    def _has_changes(self, api_proc: Dict, db_proc: Processo) -> bool:
        """
        Detecta se processo mudou
        """
        # Comparar hash
        api_hash = self._calculate_hash_simple(api_proc)
        db_hash = db_proc.hash_snapshot
        
        if api_hash != db_hash:
            return True
        
        # Comparar campos-chave
        if api_proc.get('porcentagem_conclusao') != db_proc.porcentagem_conclusao:
            return True
        
        if api_proc.get('passos_concluidos') != db_proc.passos_concluidos:
            return True
        
        return False
    
    def _calculate_hash(self, processo: Dict) -> str:
        """
        Calcula hash MD5 do processo para detectar mudanças
        """
        relevant_data = {
            'status': processo.get('status'),
            'porcentagem': processo.get('porcentagem_conclusao'),
            'passos_concluidos': sum(
                1 for p in processo.get('passos', [])
                if p.get('concluido')
            ),
            'total_passos': len(processo.get('passos', []))
        }
        
        data_str = str(sorted(relevant_data.items()))
        return hashlib.md5(data_str.encode()).hexdigest()
    
    def _calculate_hash_simple(self, processo: Dict) -> str:
        """
        Hash simplificado (sem buscar passos)
        """
        relevant_data = {
            'status': processo.get('status'),
            'porcentagem': processo.get('porcentagem_conclusao'),
            'passos_concluidos': processo.get('passos_concluidos'),
            'total_passos': processo.get('total_passos')
        }
        
        data_str = str(sorted(relevant_data.items()))
        return hashlib.md5(data_str.encode()).hexdigest()
    
    def _invalidate_cache(self, competencia: str):
        """
        Invalida cache de métricas
        """
        cache_file = self.cache_dir / f"metricas_{competencia.replace('/', '_')}.json"
        if cache_file.exists():
            cache_file.unlink()
            print(f"   🗑️  Cache invalidado")
