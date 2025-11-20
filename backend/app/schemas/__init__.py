"""
Schemas Pydantic para Validação
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# ============ EMPRESA ============
class EmpresaBase(BaseModel):
    codigo: str
    nome: str
    cnpj: Optional[str] = None
    regime_tributario: Optional[str] = None

class EmpresaCreate(EmpresaBase):
    pass

class Empresa(EmpresaBase):
    id: int
    ativa: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============ PASSO ============
class PassoBase(BaseModel):
    ordem: int
    nome: str
    descricao: Optional[str] = None
    concluido: bool = False

class Passo(PassoBase):
    id: int
    processo_id: int
    
    class Config:
        from_attributes = True

# ============ DESDOBRAMENTO ============
class DesdobramentoBase(BaseModel):
    pergunta: str
    resposta: Optional[str] = None
    alternativas: Optional[List[str]] = None
    tipo: Optional[str] = None

class Desdobramento(DesdobramentoBase):
    id: int
    processo_id: int
    respondido: bool
    
    class Config:
        from_attributes = True

# ============ PROCESSO ============
class ProcessoBase(BaseModel):
    nome: str
    competencia: str
    status: Optional[str] = None
    porcentagem_conclusao: Optional[float] = None

class ProcessoCreate(ProcessoBase):
    proc_id: int
    empresa_codigo: str
    regime_tributario: str

class ProcessoDetalhado(ProcessoBase):
    id: int
    proc_id: int
    empresa_id: int
    total_passos: Optional[int] = None
    passos_concluidos: Optional[int] = None
    dias_corridos: Optional[int] = None
    regime_tributario: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    # Relacionamentos
    passos: List[Passo] = []
    desdobramentos: List[Desdobramento] = []
    
    class Config:
        from_attributes = True

class ProcessoSimples(BaseModel):
    """Processo sem relacionamentos (para listas)"""
    id: int
    proc_id: int
    nome: str
    competencia: str
    status: Optional[str] = None
    porcentagem_conclusao: Optional[float] = None
    total_passos: Optional[int] = None
    passos_concluidos: Optional[int] = None
    dias_corridos: Optional[int] = None
    regime_tributario: Optional[str] = None
    
    class Config:
        from_attributes = True

# ============ DASHBOARD ============
class MetricasGerais(BaseModel):
    total_processos: int
    total_empresas: int
    taxa_conclusao_media: float
    regimes: dict
    ultima_atualizacao: datetime

class MetricasRegime(BaseModel):
    regime: str
    total: int
    concluidos: int
    taxa_conclusao: float
    media_dias: float

# ============ SINCRONIZAÇÃO ============
class SyncResponse(BaseModel):
    status: str
    tipo: str
    competencia: str
    processos_novos: int
    processos_atualizados: int
    tempo_execucao: int
    mensagem: str

class SyncStatus(BaseModel):
    status: str
    ultima_sincronizacao: Optional[datetime] = None
    proxima_sincronizacao: Optional[datetime] = None
    total_processos_db: int
