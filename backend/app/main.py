"""
FastAPI - Aplicação Principal
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import json
from pathlib import Path
from datetime import datetime

from .config import settings
from .database import get_db, create_tables, engine
from .models import Processo, Empresa, Sincronizacao
from .schemas import (
    ProcessoSimples,
    ProcessoDetalhado,
    MetricasGerais,
    SyncResponse,
    SyncStatus,
    Empresa as EmpresaSchema
)
from .services.acessorias_sync import AcessoriasSyncService

# Importar routers do WhatsApp
try:
    from .routers.whatsapp import router as whatsapp_router
    WHATSAPP_AVAILABLE = True
except ImportError as e:
    WHATSAPP_AVAILABLE = False
    print(f"⚠️  Módulo WhatsApp não encontrado: {e}")

# Importar router da Evolution API
try:
    from .routers.evolution import router as evolution_router
    EVOLUTION_AVAILABLE = True
except ImportError as e:
    EVOLUTION_AVAILABLE = False
    print(f"⚠️  Módulo Evolution API não encontrado: {e}")

# Criar tabelas ao iniciar
create_tables()

# Criar aplicação FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API para gestão de processos contábeis"
)

# Configurar CORS (permite frontend acessar backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção: especificar domínio do frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ REGISTRAR ROUTERS ============

# Registrar webhook do WhatsApp se disponível
if WHATSAPP_AVAILABLE:
    app.include_router(whatsapp_router, prefix="/whatsapp", tags=["WhatsApp"])
    print("✅ WhatsApp Webhook registrado em /whatsapp")

# Registrar webhook da Evolution API
if EVOLUTION_AVAILABLE:
    app.include_router(evolution_router, prefix="/whatsapp", tags=["Evolution API"])
    print("✅ Evolution API Webhook registrado em /whatsapp/evolution")

# Servir arquivos estáticos (política de privacidade)
static_dir = Path(__file__).parent.parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# ============ ENDPOINTS ============

@app.get("/privacy-policy")
def privacy_policy():
    """Política de privacidade para Meta for Developers"""
    static_file = Path(__file__).parent.parent / "static" / "privacy-policy.html"
    if static_file.exists():
        return FileResponse(static_file)
    return {"error": "Privacy policy not found"}

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }

# ============ PROCESSOS ============

@app.get(
    f"{settings.API_V1_PREFIX}/processos",
    response_model=List[ProcessoSimples],
    tags=["Processos"]
)
def listar_processos(
    competencia: Optional[str] = None,
    regime: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Lista todos os processos com filtros opcionais
    """
    query = db.query(Processo)
    
    if competencia:
        query = query.filter(Processo.competencia == competencia)
    
    if regime:
        query = query.filter(Processo.regime_tributario == regime)
    
    processos = query.offset(skip).limit(limit).all()
    return processos

@app.get(
    f"{settings.API_V1_PREFIX}/processos/{{processo_id}}",
    response_model=ProcessoDetalhado,
    tags=["Processos"]
)
def obter_processo(
    processo_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtém detalhes de um processo específico
    """
    processo = db.query(Processo).filter(Processo.id == processo_id).first()
    
    if not processo:
        raise HTTPException(status_code=404, detail="Processo não encontrado")
    
    return processo

@app.get(
    f"{settings.API_V1_PREFIX}/processos/competencia/{{competencia}}",
    response_model=List[ProcessoSimples],
    tags=["Processos"]
)
def listar_processos_competencia(
    competencia: str,
    db: Session = Depends(get_db)
):
    """
    Lista processos de uma competência específica
    """
    processos = db.query(Processo).filter(
        Processo.competencia == competencia
    ).all()
    
    return processos

# ============ EMPRESAS ============

@app.get(
    f"{settings.API_V1_PREFIX}/empresas",
    response_model=List[EmpresaSchema],
    tags=["Empresas"]
)
def listar_empresas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Lista todas as empresas
    """
    empresas = db.query(Empresa).filter(
        Empresa.ativa == True
    ).offset(skip).limit(limit).all()
    
    return empresas

@app.get(
    f"{settings.API_V1_PREFIX}/empresas/{{empresa_id}}/processos",
    response_model=List[ProcessoSimples],
    tags=["Empresas"]
)
def listar_processos_empresa(
    empresa_id: int,
    db: Session = Depends(get_db)
):
    """
    Lista processos de uma empresa específica
    """
    processos = db.query(Processo).filter(
        Processo.empresa_id == empresa_id
    ).all()
    
    return processos

# ============ DASHBOARD ============

@app.get(
    f"{settings.API_V1_PREFIX}/dashboard/metricas",
    response_model=MetricasGerais,
    tags=["Dashboard"]
)
def obter_metricas_dashboard(
    competencia: str = settings.DEFAULT_COMPETENCIA,
    db: Session = Depends(get_db)
):
    """
    Obtém métricas agregadas para o dashboard
    Com cache para performance
    """
    # Tentar cache
    cache_file = settings.CACHE_DIR / f"metricas_{competencia.replace('/', '_')}.json"
    
    if cache_file.exists():
        # Verificar se cache é válido (< 15 min)
        cache_age = datetime.now().timestamp() - cache_file.stat().st_mtime
        if cache_age < settings.CACHE_TTL:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cached_data = json.load(f)
                cached_data['ultima_atualizacao'] = datetime.fromisoformat(
                    cached_data['ultima_atualizacao']
                )
                return cached_data
    
    # Cache inválido - calcular métricas
    from sqlalchemy import func
    
    # Query otimizada
    resultados = db.query(
        Processo.regime_tributario,
        func.count(Processo.id).label('total'),
        func.count(func.nullif(Processo.status == 'CONCLUIDO', False)).label('concluidos'),
        func.avg(Processo.porcentagem_conclusao).label('media_conclusao'),
        func.avg(Processo.dias_corridos).label('media_dias'),
        func.count(func.distinct(Processo.empresa_id)).label('total_empresas')
    ).filter(
        Processo.competencia == competencia
    ).group_by(
        Processo.regime_tributario
    ).all()
    
    # Processar resultados
    total_processos = 0
    total_empresas = 0
    regimes = {}
    
    for row in resultados:
        total_processos += row.total
        total_empresas = max(total_empresas, row.total_empresas)
        
        regime_nome = row.regime_tributario or 'Não especificado'
        
        regimes[regime_nome] = {
            'total': row.total,
            'concluidos': row.concluidos or 0,
            'taxa_conclusao': round(
                (row.concluidos or 0) / row.total * 100 if row.total > 0 else 0,
                1
            ),
            'media_dias': round(row.media_dias or 0, 1),
            'percentual': round(row.total / total_processos * 100 if total_processos > 0 else 0, 1)
        }
    
    # Taxa de conclusão geral
    taxa_conclusao_media = sum(
        r['taxa_conclusao'] for r in regimes.values()
    ) / len(regimes) if regimes else 0
    
    metricas = {
        'total_processos': total_processos,
        'total_empresas': total_empresas,
        'taxa_conclusao_media': round(taxa_conclusao_media, 1),
        'regimes': regimes,
        'ultima_atualizacao': datetime.now()
    }
    
    # Salvar cache
    settings.CACHE_DIR.mkdir(exist_ok=True)
    cache_data = metricas.copy()
    cache_data['ultima_atualizacao'] = cache_data['ultima_atualizacao'].isoformat()
    
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(cache_data, f, ensure_ascii=False, indent=2)
    
    return metricas

# ============ SINCRONIZAÇÃO ============

@app.post(
    f"{settings.API_V1_PREFIX}/sync/manual",
    response_model=SyncResponse,
    tags=["Sincronização"]
)
async def sincronizar_manual(
    tipo: str = "incremental",
    competencia: str = settings.DEFAULT_COMPETENCIA,
    db: Session = Depends(get_db)
):
    """
    Trigger manual de sincronização
    - tipo: 'full' ou 'incremental'
    """
    sync_service = AcessoriasSyncService(db)
    
    if tipo == "full":
        resultado = await sync_service.sync_full(competencia)
    else:
        resultado = await sync_service.sync_incremental(competencia)
    
    return resultado

@app.get(
    f"{settings.API_V1_PREFIX}/sync/status",
    response_model=SyncStatus,
    tags=["Sincronização"]
)
def obter_status_sync(
    db: Session = Depends(get_db)
):
    """
    Status da última sincronização
    """
    ultima_sync = db.query(Sincronizacao).order_by(
        Sincronizacao.iniciada_em.desc()
    ).first()
    
    total_processos = db.query(Processo).count()
    
    return {
        'status': ultima_sync.status if ultima_sync else 'NUNCA_EXECUTADA',
        'ultima_sincronizacao': ultima_sync.iniciada_em if ultima_sync else None,
        'proxima_sincronizacao': None,  # TODO: implementar agendamento
        'total_processos_db': total_processos
    }

@app.get(
    f"{settings.API_V1_PREFIX}/sync/history",
    tags=["Sincronização"]
)
def obter_historico_sync(
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Histórico de sincronizações
    """
    historico = db.query(Sincronizacao).order_by(
        Sincronizacao.iniciada_em.desc()
    ).limit(limit).all()
    
    return [
        {
            'id': h.id,
            'tipo': h.tipo,
            'competencia': h.competencia,
            'status': h.status,
            'processos_novos': h.processos_novos,
            'processos_atualizados': h.processos_atualizados,
            'tempo_execucao': h.tempo_execucao,
            'iniciada_em': h.iniciada_em,
            'concluida_em': h.concluida_em,
            'mensagem_erro': h.mensagem_erro
        }
        for h in historico
    ]

# ============ HEALTH CHECK ============

@app.get("/health", tags=["Sistema"])
def health_check(db: Session = Depends(get_db)):
    """
    Verifica saúde do sistema
    """
    try:
        # Testa conexão com banco
        db.execute("SELECT 1")
        
        # Conta processos
        total_processos = db.query(Processo).count()
        
        return {
            'status': 'healthy',
            'database': 'connected',
            'total_processos': total_processos,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Sistema indisponível: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
