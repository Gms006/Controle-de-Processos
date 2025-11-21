"""
Gerenciador de Sincronização com API Acessórias
Busca dados e atualiza o banco SQLite local
"""
import requests
import sqlite3
import hashlib
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Dict, List, Optional
from pathlib import Path
import streamlit as st


class SyncManager:
    """Gerencia sincronização de dados com a API Acessórias"""
    
    def __init__(self, api_token: str, api_url: str = "https://api.acessorias.com", 
                 db_path: str = None):
        self.api_token = api_token
        self.api_url = api_url
        self.headers = {"Authorization": f"Bearer {api_token}"}
        
        if db_path is None:
            self.db_path = Path(__file__).parent.parent / "data" / "processos.db"
        else:
            self.db_path = Path(db_path)
    
    def sync_processos(self, competencia: str = None, 
                       regimes: List[str] = None) -> Dict:
        """
        Sincroniza processos da API para o banco local
        
        Args:
            competencia: Competência específica (ex: '2025-11')
            regimes: Lista de regimes tributários a sincronizar
        
        Returns:
            Dict com estatísticas da sincronização
        """
        if regimes is None:
            regimes = [
                'Simples Nacional — Mensal',
                'Lucro Presumido - Serviços',
                'Lucro Presumido - Comércio, Industria e Serviços',
                'Lucro Real - Comércio e Industria',
                'Lucro Real - Serviços'
            ]
        
        inicio = datetime.now()
        
        # Registrar início da sincronização
        sync_id = self._registrar_inicio_sync(competencia)
        
        try:
            processos_novos = 0
            processos_atualizados = 0
            total_processos = 0
            
            with sqlite3.connect(self.db_path) as conn:
                for regime in regimes:
                    print(f"📋 Sincronizando {regime}...")
                    
                    # Buscar processos em andamento
                    processos_andamento = self._fetch_processos(
                        proc_nome=regime,
                        proc_status="A",
                        competencia=competencia
                    )
                    
                    # Buscar processos concluídos
                    processos_concluidos = self._fetch_processos(
                        proc_nome=regime,
                        proc_status="C",
                        competencia=competencia
                    )
                    
                    processos = processos_andamento + processos_concluidos
                    print(f"  Encontrados: {len(processos)} processos")
                    
                    # Buscar detalhes completos de cada processo (ProcPassos)
                    print(f"  Buscando detalhes completos...")
                    processos_detalhados = []
                    for proc in processos:
                        proc_id = proc.get('ProcID')
                        if proc_id:
                            detalhes = self._fetch_processo_detalhado(proc_id)
                            if detalhes:
                                processos_detalhados.append(detalhes)
                    
                    print(f"  Total com detalhes: {len(processos_detalhados)}")
                    total_processos += len(processos_detalhados)
                    
                    # Salvar processos no banco
                    for proc in processos_detalhados:
                        novos, atualizados = self._salvar_processo(conn, proc)
                        processos_novos += novos
                        processos_atualizados += atualizados
                
                conn.commit()
            
            # Registrar conclusão
            tempo_exec = (datetime.now() - inicio).seconds
            self._registrar_conclusao_sync(
                sync_id, total_processos, processos_novos, 
                processos_atualizados, tempo_exec
            )
            
            return {
                "status": "CONCLUIDA",
                "total_processos": total_processos,
                "processos_novos": processos_novos,
                "processos_atualizados": processos_atualizados,
                "tempo_execucao": tempo_exec
            }
        
        except Exception as e:
            self._registrar_erro_sync(sync_id, str(e))
            raise
    
    def _fetch_processos(self, proc_nome: str, proc_status: str, 
                        competencia: str = None) -> List[Dict]:
        """Busca processos da API (lista resumida)"""
        params = {
            "ProcNome": proc_nome,
            "ProcStatus": proc_status,
            "Pagina": 1
        }
        
        if competencia:
            params["Competencia"] = competencia
        
        try:
            response = requests.get(
                f"{self.api_url}/processes/ListAll",
                headers=self.headers,
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict) and 'data' in data:
                    return data['data']
            
            return []
        
        except Exception as e:
            print(f"❌ Erro ao buscar processos: {e}")
            return []
    
    def _fetch_processo_detalhado(self, proc_id: str) -> Optional[Dict]:
        """Busca detalhes completos de um processo específico (com ProcPassos)"""
        try:
            response = requests.get(
                f"{self.api_url}/processes/{proc_id}",
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    return data[0]
                elif isinstance(data, dict):
                    return data
            
            return None
        
        except Exception as e:
            print(f"❌ Erro ao buscar detalhes do processo {proc_id}: {e}")
            return None
    
    def _salvar_processo(self, conn, proc_data: Dict) -> tuple:
        """
        Salva ou atualiza processo no banco
        
        Returns:
            (processos_novos, processos_atualizados)
        """
        # Extrair dados principais
        proc_id = proc_data.get('ProcID')
        emp_codigo = proc_data.get('EmpID')
        emp_nome = proc_data.get('EmpNome', '')
        emp_cnpj = proc_data.get('EmpCNPJ', '')
        
        # Calcular hash para detectar mudanças
        hash_atual = hashlib.md5(
            json.dumps(proc_data, sort_keys=True).encode()
        ).hexdigest()
        
        # Verificar se empresa existe
        empresa_id = self._get_or_create_empresa(
            conn, emp_codigo, emp_nome, emp_cnpj
        )
        
        # Verificar se processo já existe
        cursor = conn.execute(
            "SELECT id, hash_snapshot FROM processos WHERE proc_id = ?",
            [proc_id]
        )
        resultado = cursor.fetchone()
        
        # Calcular competência: mês anterior à data de início
        competencia = self._calcular_competencia(proc_data.get('ProcInicio'))
        
        # Contar passos
        passos = proc_data.get('ProcPassos', [])
        total_passos, passos_concluidos = self._contar_passos(passos)
        
        # Extrair porcentagem de conclusão
        porcentagem = self._extrair_porcentagem(proc_data.get('ProcPorcentagem', '0'))
        
        # Extrair dados do processo
        dados_processo = {
            'proc_id': proc_id,
            'empresa_id': empresa_id,
            'nome': proc_data.get('ProcNome', ''),
            'competencia': competencia,
            'status': proc_data.get('ProcStatus', ''),
            'porcentagem_conclusao': porcentagem,
            'total_passos': total_passos,
            'passos_concluidos': passos_concluidos,
            'dias_corridos': self._extrair_int(proc_data.get('ProcDiasCorridos', 0)),
            'data_inicio': proc_data.get('ProcInicio'),
            'data_conclusao': proc_data.get('ProcConclusao'),
            'regime_tributario': self._extrair_regime(proc_data.get('ProcNome', '')),
            'criador': proc_data.get('ProcCriador', ''),
            'gestor': proc_data.get('ProcGestor', ''),
            'departamento': proc_data.get('ProcDepartamento', ''),
            'observacoes': proc_data.get('ProcObservacoes', ''),
            'hash_snapshot': hash_atual,
            'updated_at': datetime.now().isoformat()
        }
        
        if resultado is None:
            # Inserir novo processo
            colunas = ', '.join(dados_processo.keys())
            placeholders = ', '.join(['?' for _ in dados_processo])
            
            conn.execute(
                f"INSERT INTO processos ({colunas}) VALUES ({placeholders})",
                list(dados_processo.values())
            )
            
            processo_db_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            
            # Salvar passos se houver
            self._salvar_passos(conn, processo_db_id, proc_data.get('ProcPassos', []))
            
            return (1, 0)  # 1 novo, 0 atualizado
        
        else:
            processo_db_id, hash_antigo = resultado
            
            # Atualizar apenas se houve mudança
            if hash_antigo != hash_atual:
                set_clause = ', '.join([f"{k} = ?" for k in dados_processo.keys()])
                valores = list(dados_processo.values()) + [proc_id]
                
                conn.execute(
                    f"UPDATE processos SET {set_clause} WHERE proc_id = ?",
                    valores
                )
                
                # Atualizar passos
                conn.execute("DELETE FROM passos WHERE processo_id = ?", [processo_db_id])
                self._salvar_passos(conn, processo_db_id, proc_data.get('ProcPassos', []))
                
                return (0, 1)  # 0 novo, 1 atualizado
        
        return (0, 0)  # Sem mudanças
    
    def _get_or_create_empresa(self, conn, codigo: str, nome: str, cnpj: str) -> int:
        """Retorna ID da empresa, criando se necessário"""
        cursor = conn.execute(
            "SELECT id FROM empresas WHERE codigo = ?",
            [codigo]
        )
        resultado = cursor.fetchone()
        
        if resultado:
            return resultado[0]
        
        # Criar nova empresa
        conn.execute(
            """INSERT INTO empresas (codigo, nome, cnpj) 
               VALUES (?, ?, ?)""",
            [codigo, nome, cnpj]
        )
        
        return conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    
    def _salvar_passos(self, conn, processo_id: int, passos_data: List):
        """Salva passos do processo (recursivo para sub-processos)"""
        if not passos_data:
            return
        
        # ProcPassos pode vir como [[passos]] ou [passos]
        if isinstance(passos_data, list) and len(passos_data) > 0:
            if isinstance(passos_data[0], list):
                passos_data = passos_data[0]
        
        ordem = 1
        for idx, passo in enumerate(passos_data):
            if isinstance(passo, dict):
                tipo = passo.get('Tipo', '')
                nome = passo.get('Nome', '')
                status = passo.get('Status', '')
                automacao = passo.get('Automacao', {})
                
                # Extrair responsável e bloqueante
                responsavel = ''
                bloqueante = ''
                if isinstance(automacao, dict):
                    bloqueante = automacao.get('Bloqueante', '')
                    entrega = automacao.get('Entrega', {})
                    if isinstance(entrega, dict):
                        responsavel = entrega.get('Responsavel', '')
                
                # Salvar passo
                conn.execute(
                    """INSERT INTO passos 
                       (passo_id, processo_id, ordem, nome, descricao, concluido, responsavel)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    [
                        idx,
                        processo_id,
                        ordem,
                        nome,
                        f"{tipo}: {bloqueante}" if bloqueante else tipo,
                        1 if status == 'OK' else 0,
                        responsavel
                    ]
                )
                ordem += 1
                
                # Se é desdobramento, salvar na tabela de desdobramentos
                if tipo == 'Desdobramento':
                    self._salvar_desdobramento(conn, processo_id, passo, ordem)
                
                # Se é sub-processo, processar passos filhos recursivamente
                if tipo == 'Sub processo':
                    passos_filhos = passo.get('ProcPassos', [])
                    if passos_filhos:
                        self._salvar_passos(conn, processo_id, passos_filhos)
    
    def _extrair_regime(self, proc_nome: str) -> str:
        """Extrai regime tributário do nome do processo"""
        if 'Simples' in proc_nome:
            return 'Simples Nacional'
        elif 'Presumido' in proc_nome:
            if 'Serviço' in proc_nome or 'Servico' in proc_nome:
                return 'Lucro Presumido - Serviços'
            else:
                return 'Lucro Presumido - Comércio'
        elif 'Real' in proc_nome:
            if 'Serviço' in proc_nome or 'Servico' in proc_nome:
                return 'Lucro Real - Serviços'
            else:
                return 'Lucro Real - Comércio'
        return 'Outros'
    
    def _calcular_competencia(self, data_inicio_str: str) -> str:
        """
        Calcula competência: mês ANTERIOR à data de início do processo
        Exemplo: Processo iniciado em 05/11/2025 → Competência: 2025-10
        """
        if not data_inicio_str or data_inicio_str == '0000-00-00':
            return ''
        
        try:
            # Converter de dd/mm/yyyy para datetime
            data_inicio = datetime.strptime(data_inicio_str, "%d/%m/%Y")
            
            # Calcular mês anterior
            competencia_dt = data_inicio - relativedelta(months=1)
            
            # Retornar no formato YYYY-MM
            return competencia_dt.strftime("%Y-%m")
        except Exception as e:
            print(f"⚠️  Erro ao calcular competência para {data_inicio_str}: {e}")
            return ''
    
    def _contar_passos(self, passos: List) -> tuple:
        """
        Conta total de passos e passos concluídos (recursivo)
        Returns: (total_passos, passos_concluidos)
        """
        if not passos:
            return (0, 0)
        
        # ProcPassos pode vir como [[passos]] ou [passos]
        if isinstance(passos, list) and len(passos) > 0:
            if isinstance(passos[0], list):
                passos = passos[0]
        
        total = 0
        concluidos = 0
        
        for passo in passos:
            if isinstance(passo, dict):
                total += 1
                
                # Verificar se concluído
                status = passo.get('Status', '')
                if status == 'OK':
                    concluidos += 1
                
                # Se é sub-processo, contar passos filhos recursivamente
                if passo.get('Tipo') == 'Sub processo':
                    passos_filhos = passo.get('ProcPassos', [])
                    filhos_total, filhos_concluidos = self._contar_passos(passos_filhos)
                    total += filhos_total
                    concluidos += filhos_concluidos
        
        return (total, concluidos)
    
    def _extrair_porcentagem(self, porcentagem_str: str) -> float:
        """
        Extrai porcentagem de string
        Exemplo: "45%" → 45.0, "0.00" → 0.0
        """
        if not porcentagem_str:
            return 0.0
        
        try:
            # Remover % se existir
            porcentagem_str = str(porcentagem_str).replace('%', '').strip()
            return float(porcentagem_str)
        except Exception:
            return 0.0
    
    def _extrair_int(self, valor) -> int:
        """Converte valor para inteiro com segurança"""
        try:
            return int(valor)
        except (ValueError, TypeError):
            return 0
    
    def _salvar_desdobramento(self, conn, processo_id: int, desdobramento: Dict, ordem: int):
        """Salva desdobramento na tabela de desdobramentos"""
        nome = desdobramento.get('Nome', '')
        status = desdobramento.get('Status', '')
        automacao = desdobramento.get('Automacao', [])
        
        # Extrair alternativas
        alternativas = []
        if isinstance(automacao, list):
            alternativas = [alt.get('Nome', '') for alt in automacao]
        
        alternativas_str = '; '.join(alternativas)
        
        conn.execute(
            """INSERT INTO desdobramentos 
               (desdobramento_id, processo_id, pergunta, alternativas, tipo, ordem, respondido)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            [
                ordem,
                processo_id,
                nome,
                alternativas_str,
                'Decisão',
                ordem,
                1 if status == 'OK' else 0
            ]
        )
    
    def _registrar_inicio_sync(self, competencia: str) -> int:
        """Registra início da sincronização"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """INSERT INTO sincronizacoes 
                   (tipo, competencia, status, iniciada_em)
                   VALUES (?, ?, ?, ?)""",
                ['INCREMENTAL', competencia, 'INICIADA', datetime.now().isoformat()]
            )
            conn.commit()
            return cursor.lastrowid
    
    def _registrar_conclusao_sync(self, sync_id: int, total: int, 
                                   novos: int, atualizados: int, tempo: int):
        """Registra conclusão da sincronização"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """UPDATE sincronizacoes 
                   SET status = ?, total_processos = ?, processos_novos = ?,
                       processos_atualizados = ?, tempo_execucao = ?, concluida_em = ?
                   WHERE id = ?""",
                ['CONCLUIDA', total, novos, atualizados, tempo, 
                 datetime.now().isoformat(), sync_id]
            )
            conn.commit()
    
    def _registrar_erro_sync(self, sync_id: int, erro: str):
        """Registra erro na sincronização"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """UPDATE sincronizacoes 
                   SET status = ?, mensagem_erro = ?, concluida_em = ?
                   WHERE id = ?""",
                ['ERRO', erro, datetime.now().isoformat(), sync_id]
            )
            conn.commit()
