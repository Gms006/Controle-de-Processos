"""
Gerenciador de Banco de Dados SQLite
Conecta e consulta o banco de dados de processos
"""
import sqlite3
import pandas as pd
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime
import streamlit as st


class DatabaseManager:
    """Gerencia conexão e consultas ao banco SQLite"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            # Usa o banco dentro da pasta data
            self.db_path = Path(__file__).parent.parent / "data" / "processos.db"
        else:
            self.db_path = Path(db_path)
        
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_database()
    
    def _initialize_database(self):
        """Cria tabelas se não existirem"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS empresas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo TEXT UNIQUE NOT NULL,
                    nome TEXT NOT NULL,
                    cnpj TEXT,
                    regime_tributario TEXT,
                    ativa BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS processos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    proc_id INTEGER UNIQUE NOT NULL,
                    empresa_id INTEGER,
                    nome TEXT NOT NULL,
                    competencia TEXT NOT NULL,
                    status TEXT,
                    porcentagem_conclusao REAL,
                    total_passos INTEGER,
                    passos_concluidos INTEGER,
                    dias_corridos INTEGER,
                    data_inicio TIMESTAMP,
                    data_conclusao TIMESTAMP,
                    regime_tributario TEXT,
                    criador TEXT,
                    gestor TEXT,
                    departamento TEXT,
                    observacoes TEXT,
                    hash_snapshot TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (empresa_id) REFERENCES empresas(id)
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS passos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    passo_id INTEGER NOT NULL,
                    processo_id INTEGER,
                    ordem INTEGER,
                    nome TEXT NOT NULL,
                    descricao TEXT,
                    concluido BOOLEAN DEFAULT 0,
                    responsavel TEXT,
                    data_conclusao TIMESTAMP,
                    observacoes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (processo_id) REFERENCES processos(id) ON DELETE CASCADE
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS desdobramentos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    desdobramento_id INTEGER,
                    processo_id INTEGER,
                    passo_id INTEGER,
                    pergunta TEXT NOT NULL,
                    resposta TEXT,
                    alternativas TEXT,
                    tipo TEXT,
                    ordem INTEGER,
                    respondido BOOLEAN DEFAULT 0,
                    data_resposta TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (processo_id) REFERENCES processos(id) ON DELETE CASCADE
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sincronizacoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo TEXT NOT NULL,
                    competencia TEXT,
                    total_processos INTEGER,
                    processos_novos INTEGER,
                    processos_atualizados INTEGER,
                    status TEXT,
                    mensagem_erro TEXT,
                    tempo_execucao INTEGER,
                    iniciada_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    concluida_em TIMESTAMP
                )
            """)
            
            # Criar índices para performance
            conn.execute("CREATE INDEX IF NOT EXISTS idx_processos_competencia ON processos(competencia)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_processos_status ON processos(status)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_processos_regime ON processos(regime_tributario)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_passos_concluido ON passos(concluido)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_empresas_codigo ON empresas(codigo)")
            
            conn.commit()
    
    @st.cache_data(ttl=300)  # Cache por 5 minutos
    def get_metricas_gerais(_self, competencia: str = None) -> Dict:
        """Retorna métricas agregadas do dashboard"""
        with sqlite3.connect(_self.db_path) as conn:
            where_clause = f"WHERE competencia = '{competencia}'" if competencia else ""
            
            query = f"""
                SELECT 
                    COUNT(*) as total_processos,
                    COUNT(DISTINCT empresa_id) as total_empresas,
                    AVG(porcentagem_conclusao) as media_conclusao,
                    AVG(dias_corridos) as media_dias,
                    SUM(CASE WHEN status LIKE '%Conclu%' THEN 1 ELSE 0 END) as concluidos,
                    SUM(CASE WHEN status LIKE '%Andamento%' THEN 1 ELSE 0 END) as em_andamento,
                    SUM(CASE WHEN porcentagem_conclusao = 0 THEN 1 ELSE 0 END) as parados
                FROM processos
                {where_clause}
            """
            
            result = pd.read_sql_query(query, conn).iloc[0].to_dict()
            return result
    
    @st.cache_data(ttl=300)
    def get_processos(_self, competencia: str = None, status: str = None, 
                     regime: str = None, empresa_id: int = None) -> pd.DataFrame:
        """Retorna DataFrame de processos com filtros"""
        with sqlite3.connect(_self.db_path) as conn:
            query = """
                SELECT 
                    p.proc_id,
                    e.nome as empresa,
                    e.cnpj,
                    p.nome as processo,
                    p.competencia,
                    p.status,
                    p.porcentagem_conclusao,
                    p.total_passos,
                    p.passos_concluidos,
                    p.dias_corridos,
                    p.data_inicio,
                    p.data_conclusao,
                    p.regime_tributario,
                    p.criador,
                    p.gestor,
                    p.departamento
                FROM processos p
                LEFT JOIN empresas e ON p.empresa_id = e.id
                WHERE 1=1
            """
            
            params = []
            if competencia:
                query += " AND p.competencia = ?"
                params.append(competencia)
            if status:
                query += " AND p.status LIKE ?"
                params.append(f"%{status}%")
            if regime:
                query += " AND p.regime_tributario = ?"
                params.append(regime)
            if empresa_id:
                query += " AND p.empresa_id = ?"
                params.append(empresa_id)
            
            query += " ORDER BY p.data_inicio DESC"
            
            df = pd.read_sql_query(query, conn, params=params if params else None)
            return df
    
    @st.cache_data(ttl=300)
    def get_empresas(_self) -> pd.DataFrame:
        """Retorna DataFrame de empresas"""
        with sqlite3.connect(_self.db_path) as conn:
            query = """
                SELECT 
                    e.id,
                    e.codigo,
                    e.nome,
                    e.cnpj,
                    e.regime_tributario,
                    COUNT(p.id) as total_processos,
                    AVG(p.porcentagem_conclusao) as media_conclusao,
                    AVG(p.dias_corridos) as media_dias
                FROM empresas e
                LEFT JOIN processos p ON e.id = p.empresa_id
                GROUP BY e.id, e.codigo, e.nome, e.cnpj, e.regime_tributario
                ORDER BY e.nome
            """
            return pd.read_sql_query(query, conn)
    
    @st.cache_data(ttl=300)
    def get_passos_por_processo(_self, proc_id: int) -> pd.DataFrame:
        """Retorna passos de um processo específico"""
        with sqlite3.connect(_self.db_path) as conn:
            query = """
                SELECT 
                    passo_id,
                    ordem,
                    nome,
                    descricao,
                    concluido,
                    responsavel,
                    data_conclusao,
                    observacoes
                FROM passos
                WHERE processo_id = (SELECT id FROM processos WHERE proc_id = ?)
                ORDER BY ordem
            """
            return pd.read_sql_query(query, conn, params=[proc_id])
    
    @st.cache_data(ttl=300)
    def get_analise_gargalos(_self) -> pd.DataFrame:
        """Analisa gargalos - passos mais lentos"""
        with sqlite3.connect(_self.db_path) as conn:
            query = """
                SELECT 
                    nome,
                    COUNT(*) as total_ocorrencias,
                    SUM(CASE WHEN concluido = 1 THEN 1 ELSE 0 END) as concluidos,
                    ROUND(AVG(CASE WHEN concluido = 1 THEN 1 ELSE 0 END) * 100, 2) as taxa_conclusao
                FROM passos
                GROUP BY nome
                HAVING total_ocorrencias > 5
                ORDER BY taxa_conclusao ASC, total_ocorrencias DESC
                LIMIT 20
            """
            return pd.read_sql_query(query, conn)
    
    @st.cache_data(ttl=300)
    def get_historico_sincronizacoes(_self, limit: int = 10) -> pd.DataFrame:
        """Retorna histórico de sincronizações"""
        with sqlite3.connect(_self.db_path) as conn:
            query = f"""
                SELECT 
                    tipo,
                    competencia,
                    total_processos,
                    processos_novos,
                    processos_atualizados,
                    status,
                    tempo_execucao,
                    iniciada_em,
                    concluida_em
                FROM sincronizacoes
                ORDER BY iniciada_em DESC
                LIMIT {limit}
            """
            return pd.read_sql_query(query, conn)
    
    def get_ultima_sincronizacao(self) -> Optional[Dict]:
        """Retorna dados da última sincronização"""
        with sqlite3.connect(self.db_path) as conn:
            query = """
                SELECT * FROM sincronizacoes 
                WHERE status = 'CONCLUIDA'
                ORDER BY concluida_em DESC 
                LIMIT 1
            """
            df = pd.read_sql_query(query, conn)
            if len(df) > 0:
                return df.iloc[0].to_dict()
            return None
    
    @st.cache_data(ttl=300)
    def get_competencias_disponiveis(_self) -> List[str]:
        """Retorna lista de competências disponíveis"""
        with sqlite3.connect(_self.db_path) as conn:
            query = "SELECT DISTINCT competencia FROM processos ORDER BY competencia DESC"
            df = pd.read_sql_query(query, conn)
            return df['competencia'].tolist()
    
    @st.cache_data(ttl=300)
    def get_regimes_disponiveis(_self) -> List[str]:
        """Retorna lista de regimes tributários disponíveis"""
        with sqlite3.connect(_self.db_path) as conn:
            query = "SELECT DISTINCT regime_tributario FROM processos WHERE regime_tributario IS NOT NULL ORDER BY regime_tributario"
            df = pd.read_sql_query(query, conn)
            return df['regime_tributario'].tolist()
