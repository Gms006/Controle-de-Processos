"""
Models SQLAlchemy - Banco de Dados
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class Empresa(Base):
    __tablename__ = "empresas"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(50), unique=True, nullable=False, index=True)
    nome = Column(String(255), nullable=False)
    cnpj = Column(String(18))
    regime_tributario = Column(String(50))
    ativa = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    processos = relationship("Processo", back_populates="empresa")

class Processo(Base):
    __tablename__ = "processos"
    
    id = Column(Integer, primary_key=True, index=True)
    proc_id = Column(Integer, unique=True, nullable=False, index=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id"))
    nome = Column(String(255), nullable=False)
    competencia = Column(String(7), nullable=False, index=True)
    status = Column(String(50), index=True)
    porcentagem_conclusao = Column(Float)
    total_passos = Column(Integer)
    passos_concluidos = Column(Integer)
    dias_corridos = Column(Integer)
    data_inicio = Column(DateTime)
    data_conclusao = Column(DateTime)
    regime_tributario = Column(String(50), index=True)
    hash_snapshot = Column(String(32))  # MD5 para detectar mudanças
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    empresa = relationship("Empresa", back_populates="processos")
    passos = relationship("Passo", back_populates="processo", cascade="all, delete-orphan")
    desdobramentos = relationship("Desdobramento", back_populates="processo", cascade="all, delete-orphan")

class Passo(Base):
    __tablename__ = "passos"
    
    id = Column(Integer, primary_key=True, index=True)
    passo_id = Column(Integer, nullable=False)
    processo_id = Column(Integer, ForeignKey("processos.id", ondelete="CASCADE"))
    ordem = Column(Integer)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text)
    concluido = Column(Boolean, default=False, index=True)
    responsavel = Column(String(100))
    data_conclusao = Column(DateTime)
    observacoes = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    processo = relationship("Processo", back_populates="passos")

class Desdobramento(Base):
    __tablename__ = "desdobramentos"
    
    id = Column(Integer, primary_key=True, index=True)
    desdobramento_id = Column(Integer)
    processo_id = Column(Integer, ForeignKey("processos.id", ondelete="CASCADE"))
    passo_id = Column(Integer)
    pergunta = Column(Text, nullable=False)
    resposta = Column(Text)
    alternativas = Column(JSON)  # Lista de opções
    tipo = Column(String(50))  # 'BINARIO', 'MULTIPLA_ESCOLHA'
    ordem = Column(Integer)
    respondido = Column(Boolean, default=False, index=True)
    data_resposta = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    processo = relationship("Processo", back_populates="desdobramentos")

class Sincronizacao(Base):
    __tablename__ = "sincronizacoes"
    
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(50), nullable=False, index=True)  # 'FULL', 'INCREMENTAL'
    competencia = Column(String(7), index=True)
    total_processos = Column(Integer)
    processos_novos = Column(Integer)
    processos_atualizados = Column(Integer)
    status = Column(String(50), index=True)  # 'INICIADA', 'CONCLUIDA', 'ERRO'
    mensagem_erro = Column(Text)
    tempo_execucao = Column(Integer)  # segundos
    iniciada_em = Column(DateTime, server_default=func.now())
    concluida_em = Column(DateTime)
