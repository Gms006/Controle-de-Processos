# 🏗️ ARQUITETURA BACKEND + FRONTEND + BANCO DE DADOS

## 📋 Visão Geral

### Stack Tecnológica Proposta

**Backend (API REST)**
- **Framework**: FastAPI (Python)
- **Banco de Dados**: PostgreSQL (produção) / SQLite (desenvolvimento)
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Cache**: Redis (opcional, para cache de consultas)
- **Task Queue**: Celery + Redis (para sincronização em background)

**Frontend (SPA - Single Page Application)**
- **Framework**: React.js com TypeScript
- **UI Library**: Material-UI (MUI) ou Ant Design
- **State Management**: React Query (cache + sincronização automática)
- **Charts**: Recharts ou Chart.js
- **Build Tool**: Vite

**Infraestrutura**
- **Containerização**: Docker + Docker Compose
- **Deploy Backend**: Railway / Render / Fly.io (free tier)
- **Deploy Frontend**: Vercel / Netlify (free tier)
- **CI/CD**: GitHub Actions

---

## 🗄️ Modelagem do Banco de Dados

### Tabelas Principais

```sql
-- 1. EMPRESAS
CREATE TABLE empresas (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    nome VARCHAR(255) NOT NULL,
    cnpj VARCHAR(18),
    regime_tributario VARCHAR(50),
    ativa BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 2. PROCESSOS
CREATE TABLE processos (
    id SERIAL PRIMARY KEY,
    proc_id INTEGER UNIQUE NOT NULL,  -- ID da API Acessórias
    empresa_id INTEGER REFERENCES empresas(id),
    nome VARCHAR(255) NOT NULL,
    competencia VARCHAR(7) NOT NULL,  -- '10/2025'
    status VARCHAR(50),  -- 'EM_ANDAMENTO', 'CONCLUIDO', 'PENDENTE'
    porcentagem_conclusao DECIMAL(5,2),
    total_passos INTEGER,
    passos_concluidos INTEGER,
    dias_corridos INTEGER,
    data_inicio TIMESTAMP,
    data_conclusao TIMESTAMP,
    regime_tributario VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_competencia (competencia),
    INDEX idx_status (status),
    INDEX idx_empresa (empresa_id)
);

-- 3. PASSOS (Steps)
CREATE TABLE passos (
    id SERIAL PRIMARY KEY,
    passo_id INTEGER NOT NULL,  -- ID da API
    processo_id INTEGER REFERENCES processos(id) ON DELETE CASCADE,
    ordem INTEGER,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    concluido BOOLEAN DEFAULT false,
    responsavel VARCHAR(100),
    data_conclusao TIMESTAMP,
    observacoes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_processo (processo_id),
    INDEX idx_concluido (concluido)
);

-- 4. DESDOBRAMENTOS
CREATE TABLE desdobramentos (
    id SERIAL PRIMARY KEY,
    desdobramento_id INTEGER,
    passo_id INTEGER REFERENCES passos(id) ON DELETE CASCADE,
    processo_id INTEGER REFERENCES processos(id) ON DELETE CASCADE,
    pergunta TEXT NOT NULL,
    resposta TEXT,
    alternativas JSONB,  -- Array de opções
    tipo VARCHAR(50),  -- 'BINARIO', 'MULTIPLA_ESCOLHA'
    ordem INTEGER,
    respondido BOOLEAN DEFAULT false,
    data_resposta TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_processo (processo_id),
    INDEX idx_respondido (respondido)
);

-- 5. OBRIGACOES (DAS, EFD REINF, etc)
CREATE TABLE obrigacoes (
    id SERIAL PRIMARY KEY,
    processo_id INTEGER REFERENCES processos(id) ON DELETE CASCADE,
    tipo VARCHAR(100) NOT NULL,  -- 'DAS', 'EFD_REINF', 'DIFAL', etc
    descricao TEXT,
    status VARCHAR(50),  -- 'PENDENTE', 'ENTREGUE', 'DISPENSADO'
    data_vencimento DATE,
    data_entrega TIMESTAMP,
    valor DECIMAL(15,2),
    codigo_recibo VARCHAR(100),
    arquivo_url TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_tipo (tipo),
    INDEX idx_status (status),
    INDEX idx_vencimento (data_vencimento)
);

-- 6. SINCRONIZACOES (Log de atualizações)
CREATE TABLE sincronizacoes (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL,  -- 'FULL', 'INCREMENTAL', 'MANUAL'
    competencia VARCHAR(7),
    total_processos INTEGER,
    processos_novos INTEGER,
    processos_atualizados INTEGER,
    status VARCHAR(50),  -- 'INICIADA', 'CONCLUIDA', 'ERRO'
    mensagem_erro TEXT,
    tempo_execucao INTEGER,  -- segundos
    iniciada_em TIMESTAMP DEFAULT NOW(),
    concluida_em TIMESTAMP,
    
    INDEX idx_tipo (tipo),
    INDEX idx_status (status),
    INDEX idx_competencia (competencia)
);

-- 7. USUARIOS (para autenticação futura)
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    nome VARCHAR(255) NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'USER',  -- 'ADMIN', 'MANAGER', 'USER'
    ativo BOOLEAN DEFAULT true,
    ultimo_acesso TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 8. METRICAS_CACHE (para dashboards rápidos)
CREATE TABLE metricas_cache (
    id SERIAL PRIMARY KEY,
    competencia VARCHAR(7) NOT NULL,
    regime_tributario VARCHAR(50),
    metrica_tipo VARCHAR(100) NOT NULL,  -- 'TOTAL_PROCESSOS', 'TAXA_CONCLUSAO', etc
    valor JSONB NOT NULL,  -- Armazena objeto com valores
    calculada_em TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(competencia, regime_tributario, metrica_tipo),
    INDEX idx_competencia (competencia),
    INDEX idx_tipo (metrica_tipo)
);
```

---

## 🔄 Estratégia de Sincronização Otimizada

### 1. **Sincronização Inicial (FULL SYNC)**
```python
# Primeira vez - busca tudo
- Buscar todos os 211 processos da API
- Inserir no banco de dados
- Marcar última sincronização
- Calcular métricas iniciais
```

### 2. **Sincronização Incremental (SMART SYNC)**
```python
# Estratégia otimizada:

1. VERIFICAÇÃO RÁPIDA (a cada 15 min)
   - Buscar apenas METADATA dos processos (sem passos)
   - Comparar hash/timestamp com banco local
   - Identificar processos modificados
   
2. ATUALIZAÇÃO SELETIVA
   - Buscar APENAS processos que mudaram
   - Atualizar registros específicos
   - Evitar sobrecarga da API
   
3. LÓGICA DE DETECÇÃO DE MUDANÇAS:
   - Campo 'updated_at' na API
   - Comparar porcentagem de conclusão
   - Verificar total de passos concluídos
   
4. CACHE INTELIGENTE
   - Métricas calculadas ficam em cache (tabela metricas_cache)
   - Recalcula apenas quando há mudanças
   - Dashboard lê do cache (sub-segundo)
```

### 3. **Sincronização em Background (CELERY TASKS)**
```python
# Tasks assíncronas:

@celery.task
def sync_processos_incremental():
    """Roda a cada 15 minutos"""
    1. Buscar lista de processos (lightweight)
    2. Comparar com banco
    3. Atualizar apenas os modificados
    4. Invalidar cache de métricas
    
@celery.task
def sync_full_competencia(competencia):
    """Sincronização completa manual"""
    1. Buscar todos os processos
    2. Truncar dados antigos (opcional)
    3. Reinserir tudo
    4. Recalcular métricas

@celery.task
def calcular_metricas_diarias():
    """Roda 1x por dia às 00:00"""
    1. Calcular estatísticas agregadas
    2. Atualizar tabela metricas_cache
    3. Gerar relatórios automáticos
```

---

## 🚀 Arquitetura da API (FastAPI)

### Estrutura de Diretórios

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # Ponto de entrada FastAPI
│   ├── config.py                  # Configurações (env vars)
│   ├── database.py                # Conexão DB + SessionLocal
│   │
│   ├── models/                    # SQLAlchemy Models
│   │   ├── __init__.py
│   │   ├── empresa.py
│   │   ├── processo.py
│   │   ├── passo.py
│   │   ├── desdobramento.py
│   │   ├── obrigacao.py
│   │   └── sincronizacao.py
│   │
│   ├── schemas/                   # Pydantic Schemas (validação)
│   │   ├── __init__.py
│   │   ├── processo.py
│   │   ├── dashboard.py
│   │   └── sync.py
│   │
│   ├── crud/                      # CRUD operations
│   │   ├── __init__.py
│   │   ├── processo.py
│   │   ├── empresa.py
│   │   └── metricas.py
│   │
│   ├── api/                       # Endpoints
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── processos.py       # GET /processos, /processos/{id}
│   │   │   ├── dashboard.py       # GET /dashboard/metricas
│   │   │   ├── sync.py            # POST /sync/manual
│   │   │   └── empresas.py        # GET /empresas
│   │
│   ├── services/                  # Lógica de negócio
│   │   ├── __init__.py
│   │   ├── acessorias_sync.py     # Sincronização com API
│   │   ├── metricas_service.py    # Cálculo de métricas
│   │   └── cache_service.py       # Gestão de cache
│   │
│   ├── tasks/                     # Celery tasks
│   │   ├── __init__.py
│   │   ├── sync_tasks.py
│   │   └── metricas_tasks.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── rate_limiter.py
│       └── logger.py
│
├── alembic/                       # Migrations
│   ├── versions/
│   └── env.py
│
├── tests/
│   ├── test_api.py
│   └── test_sync.py
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

### Endpoints da API

```
# PROCESSOS
GET    /api/v1/processos                    # Lista todos (paginado)
GET    /api/v1/processos/{id}               # Detalhes de 1 processo
GET    /api/v1/processos/competencia/{comp} # Filtra por competência
GET    /api/v1/processos/empresa/{emp_id}   # Processos de 1 empresa
GET    /api/v1/processos/{id}/passos        # Passos do processo
GET    /api/v1/processos/{id}/desdobramentos # Desdobramentos

# DASHBOARD
GET    /api/v1/dashboard/metricas           # Métricas gerais (cached)
GET    /api/v1/dashboard/regimes            # Estatísticas por regime
GET    /api/v1/dashboard/timeline           # Histórico temporal

# SINCRONIZAÇÃO
POST   /api/v1/sync/manual                  # Trigger sync manual
GET    /api/v1/sync/status                  # Status da última sync
GET    /api/v1/sync/history                 # Histórico de syncs

# EMPRESAS
GET    /api/v1/empresas                     # Lista empresas
GET    /api/v1/empresas/{id}/processos      # Processos da empresa

# OBRIGAÇÕES
GET    /api/v1/obrigacoes                   # Lista obrigações
GET    /api/v1/obrigacoes/vencimento/{data} # Por vencimento
```

---

## 🎨 Arquitetura do Frontend (React)

### Estrutura de Diretórios

```
frontend/
├── public/
│   └── index.html
│
├── src/
│   ├── main.tsx                   # Entry point
│   ├── App.tsx                    # Root component
│   │
│   ├── components/                # Componentes reutilizáveis
│   │   ├── Layout/
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── Footer.tsx
│   │   │
│   │   ├── Dashboard/
│   │   │   ├── StatCard.tsx
│   │   │   ├── RegimeChart.tsx
│   │   │   ├── TimelineChart.tsx
│   │   │   └── MetricasGerais.tsx
│   │   │
│   │   ├── Processos/
│   │   │   ├── ProcessosList.tsx
│   │   │   ├── ProcessoCard.tsx
│   │   │   ├── ProcessoDetail.tsx
│   │   │   └── PassosList.tsx
│   │   │
│   │   └── Common/
│   │       ├── LoadingSpinner.tsx
│   │       ├── ErrorBoundary.tsx
│   │       └── Pagination.tsx
│   │
│   ├── pages/                     # Páginas/Rotas
│   │   ├── DashboardPage.tsx
│   │   ├── ProcessosPage.tsx
│   │   ├── ProcessoDetailPage.tsx
│   │   ├── EmpresasPage.tsx
│   │   └── SyncPage.tsx
│   │
│   ├── services/                  # API calls
│   │   ├── api.ts                 # Axios config
│   │   ├── processosService.ts
│   │   ├── dashboardService.ts
│   │   └── syncService.ts
│   │
│   ├── hooks/                     # Custom React hooks
│   │   ├── useProcessos.ts
│   │   ├── useDashboard.ts
│   │   └── useSync.ts
│   │
│   ├── contexts/                  # React Context
│   │   ├── AuthContext.tsx
│   │   └── ThemeContext.tsx
│   │
│   ├── types/                     # TypeScript types
│   │   ├── processo.ts
│   │   ├── dashboard.ts
│   │   └── empresa.ts
│   │
│   ├── utils/
│   │   ├── formatters.ts
│   │   └── constants.ts
│   │
│   └── styles/
│       └── theme.ts               # MUI theme customization
│
├── package.json
├── tsconfig.json
├── vite.config.ts
└── Dockerfile
```

### Exemplo de Component (StatCard.tsx)

```typescript
import { Card, CardContent, Typography, Box } from '@mui/material';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';

interface StatCardProps {
  label: string;
  value: number | string;
  icon: React.ReactNode;
  color: string;
  trend?: number;
}

export const StatCard: React.FC<StatCardProps> = ({
  label,
  value,
  icon,
  color,
  trend
}) => {
  return (
    <Card sx={{ 
      background: `linear-gradient(135deg, ${color}22 0%, ${color}44 100%)`,
      transition: 'transform 0.3s',
      '&:hover': { transform: 'translateY(-5px)' }
    }}>
      <CardContent>
        <Box display="flex" justifyContent="space-between">
          <Box>
            <Typography variant="caption" color="textSecondary">
              {label}
            </Typography>
            <Typography variant="h3" fontWeight="bold">
              {value}
            </Typography>
          </Box>
          <Box sx={{ color }}>{icon}</Box>
        </Box>
        {trend && (
          <Box display="flex" alignItems="center" mt={1}>
            <TrendingUpIcon fontSize="small" />
            <Typography variant="caption" ml={0.5}>
              +{trend}% vs. mês anterior
            </Typography>
          </Box>
        )}
      </CardContent>
    </Card>
  );
};
```

---

## 🔄 Lógica de Sincronização Otimizada

### Algoritmo de Detecção de Mudanças

```python
# backend/app/services/acessorias_sync.py

from datetime import datetime
from typing import List, Dict
import hashlib

class AcessoriasSyncService:
    
    async def sync_incremental(self, competencia: str) -> Dict:
        """
        Sincronização incremental otimizada
        """
        start_time = datetime.now()
        
        # 1. Buscar lista resumida da API (LEVE)
        api_processos = await self.fetch_processos_metadata(competencia)
        
        # 2. Buscar processos existentes no banco
        db_processos = await self.get_processos_from_db(competencia)
        
        # 3. Comparar e identificar mudanças
        novos = []
        atualizados = []
        
        for api_proc in api_processos:
            db_proc = db_processos.get(api_proc['proc_id'])
            
            if not db_proc:
                # Processo novo
                novos.append(api_proc['proc_id'])
            elif self.has_changes(api_proc, db_proc):
                # Processo modificado
                atualizados.append(api_proc['proc_id'])
        
        # 4. Buscar DETALHES apenas dos processos que mudaram
        if novos or atualizados:
            processos_ids = novos + atualizados
            
            # Busca em paralelo (max 5 simultâneos para não sobrecarregar)
            processos_detalhados = await self.fetch_processos_batch(
                processos_ids,
                batch_size=5
            )
            
            # 5. Atualizar banco de dados
            await self.upsert_processos(processos_detalhados)
            
            # 6. Invalidar cache de métricas
            await self.invalidate_metrics_cache(competencia)
        
        # 7. Registrar sincronização
        tempo_execucao = (datetime.now() - start_time).seconds
        await self.log_sync(
            tipo='INCREMENTAL',
            competencia=competencia,
            processos_novos=len(novos),
            processos_atualizados=len(atualizados),
            tempo_execucao=tempo_execucao
        )
        
        return {
            'status': 'CONCLUIDA',
            'novos': len(novos),
            'atualizados': len(atualizados),
            'tempo_execucao': tempo_execucao
        }
    
    def has_changes(self, api_proc: Dict, db_proc: Dict) -> bool:
        """
        Detecta se processo mudou comparando campos-chave
        """
        # Estratégia 1: Comparar hash
        api_hash = self.calculate_hash(api_proc)
        db_hash = db_proc.get('hash_snapshot')
        
        if api_hash != db_hash:
            return True
        
        # Estratégia 2: Comparar campos específicos
        if api_proc.get('porcentagem_conclusao') != db_proc.get('porcentagem_conclusao'):
            return True
        
        if api_proc.get('passos_concluidos') != db_proc.get('passos_concluidos'):
            return True
        
        # Estratégia 3: Verificar timestamp (se API fornecer)
        if api_proc.get('updated_at'):
            api_updated = datetime.fromisoformat(api_proc['updated_at'])
            db_updated = db_proc.get('updated_at')
            if api_updated > db_updated:
                return True
        
        return False
    
    def calculate_hash(self, processo: Dict) -> str:
        """
        Gera hash do processo para detectar mudanças
        """
        # Campos relevantes para comparação
        relevant_data = {
            'status': processo.get('status'),
            'porcentagem': processo.get('porcentagem_conclusao'),
            'passos_concluidos': processo.get('passos_concluidos'),
            'total_passos': processo.get('total_passos')
        }
        
        data_str = str(sorted(relevant_data.items()))
        return hashlib.md5(data_str.encode()).hexdigest()
    
    async def fetch_processos_batch(
        self,
        processos_ids: List[int],
        batch_size: int = 5
    ) -> List[Dict]:
        """
        Busca processos em lotes paralelos
        """
        import asyncio
        
        processos = []
        
        # Divide em lotes
        for i in range(0, len(processos_ids), batch_size):
            batch = processos_ids[i:i + batch_size]
            
            # Busca paralela
            tasks = [
                self.fetch_processo_detail(proc_id)
                for proc_id in batch
            ]
            batch_results = await asyncio.gather(*tasks)
            processos.extend(batch_results)
            
            # Rate limiting - pausa entre batches
            await asyncio.sleep(1)
        
        return processos
```

---

## 📊 Cache de Métricas

```python
# backend/app/services/metricas_service.py

class MetricasService:
    
    async def get_dashboard_metricas(self, competencia: str) -> Dict:
        """
        Busca métricas do cache ou calcula se necessário
        """
        # 1. Tentar buscar do cache
        cached = await self.get_from_cache(competencia, 'METRICAS_GERAIS')
        
        if cached and self.is_cache_valid(cached):
            return cached['valor']
        
        # 2. Cache inválido - recalcular
        metricas = await self.calcular_metricas(competencia)
        
        # 3. Salvar no cache
        await self.save_to_cache(
            competencia=competencia,
            metrica_tipo='METRICAS_GERAIS',
            valor=metricas
        )
        
        return metricas
    
    async def calcular_metricas(self, competencia: str) -> Dict:
        """
        Calcula todas as métricas do zero
        """
        # Queries otimizadas no banco
        query = """
        SELECT 
            COUNT(*) as total_processos,
            SUM(CASE WHEN status = 'CONCLUIDO' THEN 1 ELSE 0 END) as concluidos,
            AVG(porcentagem_conclusao) as media_conclusao,
            AVG(dias_corridos) as media_dias,
            regime_tributario,
            COUNT(DISTINCT empresa_id) as total_empresas
        FROM processos
        WHERE competencia = :competencia
        GROUP BY regime_tributario
        """
        
        result = await self.db.execute(query, {'competencia': competencia})
        
        # Processar resultados
        metricas = {
            'total_processos': 0,
            'total_empresas': 0,
            'taxa_conclusao': 0,
            'regimes': {}
        }
        
        for row in result:
            metricas['total_processos'] += row.total_processos
            metricas['total_empresas'] += row.total_empresas
            
            metricas['regimes'][row.regime_tributario] = {
                'total': row.total_processos,
                'concluidos': row.concluidos,
                'taxa_conclusao': (row.concluidos / row.total_processos * 100) if row.total_processos > 0 else 0,
                'media_dias': round(row.media_dias, 1)
            }
        
        return metricas
```

---

## 🐳 Docker Compose

```yaml
# docker-compose.yml

version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: acessorias_db
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: senha_segura
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  backend:
    build: ./backend
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://admin:senha_segura@postgres:5432/acessorias_db
      REDIS_URL: redis://redis:6379/0
      ACESSORIAS_API_TOKEN: ${ACESSORIAS_API_TOKEN}
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started

  celery_worker:
    build: ./backend
    command: celery -A app.tasks worker --loglevel=info
    volumes:
      - ./backend:/app
    environment:
      DATABASE_URL: postgresql://admin:senha_segura@postgres:5432/acessorias_db
      REDIS_URL: redis://redis:6379/0
      ACESSORIAS_API_TOKEN: ${ACESSORIAS_API_TOKEN}
    depends_on:
      - postgres
      - redis

  celery_beat:
    build: ./backend
    command: celery -A app.tasks beat --loglevel=info
    volumes:
      - ./backend:/app
    environment:
      DATABASE_URL: postgresql://admin:senha_segura@postgres:5432/acessorias_db
      REDIS_URL: redis://redis:6379/0
    depends_on:
      - postgres
      - redis

  frontend:
    build: ./frontend
    command: npm run dev
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "5173:5173"
    environment:
      VITE_API_URL: http://localhost:8000/api/v1

volumes:
  postgres_data:
  redis_data:
```

---

## 📈 Estimativa de Performance

### Sincronização Inicial (211 processos)
- **Tempo**: ~3-5 minutos
- **API Calls**: 212 (1 lista + 211 detalhes)
- **Inserções DB**: ~2.000 registros (processos + passos + desdobramentos)

### Sincronização Incremental (típica)
- **Tempo**: ~10-30 segundos
- **API Calls**: 1-15 (apenas processos modificados)
- **Updates DB**: ~50-200 registros

### Dashboard (com cache)
- **Tempo de resposta**: < 100ms
- **Leitura do cache**: ~10ms
- **Sem cache**: ~500ms (recalcula tudo)

---

## 🎯 Próximos Passos Implementação

### Fase 1 - Backend Core (3 dias)
1. ✅ Criar estrutura FastAPI
2. ✅ Modelar banco de dados (SQLAlchemy)
3. ✅ Implementar migrations (Alembic)
4. ✅ Criar endpoints básicos
5. ✅ Implementar serviço de sincronização

### Fase 2 - Sincronização Inteligente (2 dias)
1. ✅ Lógica de detecção de mudanças
2. ✅ Sistema de cache de métricas
3. ✅ Celery tasks para sync em background
4. ✅ Rate limiting e retries

### Fase 3 - Frontend React (3 dias)
1. ✅ Setup Vite + React + TypeScript
2. ✅ Componentes de dashboard
3. ✅ Integração com API (React Query)
4. ✅ Charts e visualizações

### Fase 4 - Deploy (1 dia)
1. ✅ Docker Compose local
2. ✅ Deploy backend (Railway)
3. ✅ Deploy frontend (Vercel)
4. ✅ CI/CD com GitHub Actions

### Fase 5 - WhatsApp Integration (2 dias)
1. ✅ Webhook do WhatsApp
2. ✅ Comandos de consulta
3. ✅ Notificações automáticas

---

## 💰 Custo Estimado

- **PostgreSQL**: Railway (FREE até 500MB) ou Supabase (FREE até 500MB)
- **Backend**: Railway (FREE com $5 crédito/mês)
- **Frontend**: Vercel (FREE ilimitado para hobby)
- **Redis**: Railway (FREE até 25MB)
- **Total**: **R$ 0/mês** (tier free) ou **~R$ 25/mês** (produção)

---

**Quer que eu comece a implementar? Posso criar:**
1. Backend completo com FastAPI + PostgreSQL
2. Frontend React com dashboard interativo
3. Sistema de sincronização inteligente
4. Docker Compose para rodar tudo local

**Qual parte você quer que eu desenvolva primeiro?**
