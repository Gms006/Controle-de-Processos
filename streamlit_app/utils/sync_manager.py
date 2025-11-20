"""
Gerenciador de Sincronização com API Acessórias
Busca dados e atualiza o banco SQLite local
"""
import requests
import sqlite3
import hashlib
import json
from datetime import datetime
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
                    total_processos += len(processos)
                    
                    # Salvar processos no banco
                    for proc in processos:
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
        """Busca processos da API"""
        params = {
            "ProcNome": proc_nome,
            "ProcStatus": proc_status
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
        
        # Extrair dados do processo
        dados_processo = {
            'proc_id': proc_id,
            'empresa_id': empresa_id,
            'nome': proc_data.get('ProcNome', ''),
            'competencia': proc_data.get('ProcCompetencia', ''),
            'status': proc_data.get('ProcStatus', ''),
            'porcentagem_conclusao': proc_data.get('ProcPorcentagem', 0),
            'total_passos': proc_data.get('ProcTotalPassos', 0),
            'passos_concluidos': proc_data.get('ProcPassosConcluidos', 0),
            'dias_corridos': proc_data.get('ProcDiasCorridos', 0),
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
        """Salva passos do processo"""
        if not passos_data:
            return
        
        # ProcPassos pode vir como [[passos]] ou [passos]
        if isinstance(passos_data, list) and len(passos_data) > 0:
            if isinstance(passos_data[0], list):
                passos_data = passos_data[0]
        
        for idx, passo in enumerate(passos_data):
            if isinstance(passo, dict):
                conn.execute(
                    """INSERT INTO passos 
                       (passo_id, processo_id, ordem, nome, descricao, concluido, responsavel)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    [
                        passo.get('PassoID', idx),
                        processo_id,
                        idx + 1,
                        passo.get('PassoNome', ''),
                        passo.get('PassoDescricao', ''),
                        1 if passo.get('PassoConcluido') else 0,
                        passo.get('PassoResponsavel', '')
                    ]
                )
    
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
