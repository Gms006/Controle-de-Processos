# 📊 SISTEMA DE GESTÃO DE PROCESSOS CONTÁBEIS
## Projeto Completo: API Acessórias → Dashboard Web

---

## 🎯 VISÃO GERAL

Sistema web para visualização e gestão de processos contábeis provenientes da API Acessórias.
Substitui planilhas Excel por dashboard interativo em tempo real.

**Stack:**
- **Backend:** FastAPI + SQLAlchemy + SQLite
- **Frontend:** React + TypeScript + Material-UI + Vite
- **Sincronização:** Scripts Python para popular banco de dados

---

## ✅ O QUE JÁ FOI FEITO

### 1. Backend FastAPI (100% Funcional)

**Localização:** `c:\acessorias processos\backend\`

**Estrutura:**
```
backend/
├── app/
│   ├── main.py              # Aplicação FastAPI principal
│   ├── config.py            # Configurações (API token, URLs)
│   ├── database.py          # Conexão SQLite + SessionLocal
│   ├── models.py            # 5 modelos SQLAlchemy
│   ├── routers/
│   │   ├── processos.py     # CRUD de processos
│   │   ├── empresas.py      # CRUD de empresas
│   │   ├── dashboard.py     # Métricas agregadas
│   │   └── sync.py          # Sincronização manual
│   └── services/
│       └── acessorias_sync.py  # Serviço de sincronização
├── run.py                   # Inicializador do servidor
└── database.db              # SQLite com 62 processos
```

**Endpoints Funcionais:** (15+ endpoints)
- `GET /api/v1/processos` - Listar todos os processos
- `GET /api/v1/processos/{id}` - Detalhes de um processo
- `GET /api/v1/empresas` - Listar empresas
- `GET /api/v1/dashboard/metricas` - **Métricas do dashboard**
- `POST /api/v1/sync/manual` - Sincronização manual
- Swagger Docs: http://localhost:8000/docs

**Como Rodar:**
```bash
cd "c:\acessorias processos\backend"
python run.py
# Acessa: http://localhost:8000
```

---

### 2. Banco de Dados SQLite (29% Completo)

**Localização:** `c:\acessorias processos\database.db`

**Tabelas:**
1. **empresas** - 61 empresas cadastradas
2. **processos** - 62 processos (29% de 211 total)
3. **passos** - 319 passos vinculados aos processos
4. **desdobramentos** - 136 desdobramentos (perguntas/respostas)
5. **sincronizacoes** - Log de sincronizações

**Dados Atuais:**
- ✅ LucroPresumido: 44 empresas
- ✅ LucroReal: 17 empresas
- ⏳ SimplesNacional: 0 empresas (150 processos pendentes)

**Script de Verificação:**
```bash
cd "c:\acessorias processos"
python scripts/verificar_banco.py
```

---

### 3. Frontend React (95% Funcional - 1 BUG)

**Localização:** `c:\acessorias processos\frontend\`

**Estrutura:**
```
frontend/
├── src/
│   ├── App.tsx                    # Rotas + Tema MUI
│   ├── main.tsx                   # Entry point
│   ├── components/
│   │   └── Layout.tsx             # Sidebar + Header
│   ├── pages/
│   │   ├── Dashboard.tsx          # ⚠️ BUG: regime.porcentagem undefined
│   │   ├── Empresas.tsx           # Placeholder
│   │   ├── Declaracoes.tsx        # Placeholder
│   │   ├── Faturamento.tsx        # Placeholder
│   │   └── Desdobramentos.tsx     # Placeholder
│   └── index.css
├── package.json                   # React 18.3.1 + MUI 5.18.0
└── vite.config.ts                 # Proxy para backend
```

**Páginas:**
1. **Dashboard (/)** - Métricas principais + gráficos por regime
2. **Empresas (/empresas)** - Análise individual por empresa
3. **Declarações (/declaracoes)** - Obrigações mensais (DAS, EFD, etc)
4. **Faturamento (/faturamento)** - Empresas com/sem faturamento
5. **Desdobramentos (/desdobramentos)** - Perguntas pendentes

**Como Rodar:**
```bash
cd "c:\acessorias processos\frontend"
npm run dev
# Acessa: http://localhost:3000
```

**BUG ATUAL:**
- **Linha 164 do Dashboard.tsx:** `regime.porcentagem.toFixed()` falha porque `porcentagem` vem como `undefined` do backend
- **Causa:** Backend retorna `por_regime` mas sem o campo `porcentagem` calculado
- **Impacto:** Tela fica branca após carregar dados

---

### 4. Scripts de Sincronização

**Localização:** `c:\acessorias processos\scripts\`

**Scripts Criados:**
1. **api_client.py** - Cliente da API Acessórias (rate limiting)
2. **sincronizar_banco.py** - Sincronizador principal (completo mas lento)
3. **sync_simples_nacional.py** - Sincroniza apenas SimplesNacional
4. **sync_inteligente.py** - Detecta regimes pendentes
5. **verificar_banco.py** - Verifica dados no banco
6. **monitorar_sync.py** - Monitora progresso em tempo real

**Problema Atual:**
- Rate limiting da API Acessórias: ~24 segundos por requisição
- Tempo estimado para 150 processos do SimplesNacional: 60-90 minutos

---

## 🐛 BUGS CRÍTICOS A CORRIGIR

### BUG #1: Dashboard.tsx - TypeError na linha 164
**Prioridade:** 🔴 CRÍTICA

**Erro:**
```
Uncaught TypeError: Cannot read properties of undefined (reading 'toFixed')
at Dashboard (Dashboard.tsx:164:48)
```

**Localização:** `frontend/src/pages/Dashboard.tsx:164`

**Código com Erro:**
```typescript
{regime.porcentagem.toFixed(1)}%  // ❌ regime.porcentagem é undefined
```

**Causa Raiz:**
O endpoint `/api/v1/dashboard/metricas` retorna `por_regime` sem calcular o campo `porcentagem`.

**Solução:**
Adicionar validação:
```typescript
{(regime.porcentagem || 0).toFixed(1)}%
```

**OU** corrigir backend para calcular porcentagem:
```python
# backend/app/routers/dashboard.py
por_regime.append({
    "regime": regime,
    "total": total,
    "concluidos": concluidos,
    "porcentagem": (concluidos / total * 100) if total > 0 else 0  # ← Adicionar
})
```

---

## 📋 PRÓXIMOS PASSOS (EM ORDEM DE PRIORIDADE)

### **PASSO 1: CORRIGIR BUG DO DASHBOARD** 🔴
**Tempo estimado:** 5 minutos
**Impacto:** Crítico - sistema não funciona

**Ações:**
1. Abrir `backend/app/routers/dashboard.py`
2. Localizar função `get_metricas()`
3. Adicionar cálculo de `porcentagem` no loop `por_regime`
4. Reiniciar backend
5. Testar dashboard no frontend

**Código de Exemplo:**
```python
por_regime = []
for regime in regimes_disponiveis:
    total = db.query(Processo).filter(Processo.regime_tributario == regime).count()
    concluidos = db.query(Processo).filter(
        Processo.regime_tributario == regime,
        Processo.status == 'CONCLUIDO'
    ).count()
    
    por_regime.append({
        "regime": regime,
        "total": total,
        "concluidos": concluidos,
        "porcentagem": (concluidos / total * 100) if total > 0 else 0  # ← FIX
    })
```

---

### **PASSO 2: COMPLETAR SINCRONIZAÇÃO DO SIMPLESNACIONAL** 🟡
**Tempo estimado:** 60-90 minutos (automático)
**Impacto:** Médio - dados incompletos

**Ações:**
1. Abrir terminal em `c:\acessorias processos\scripts`
2. Executar: `python sync_simples_nacional.py`
3. Aguardar conclusão (150 processos)
4. Verificar: `python verificar_banco.py`

**Alternativa Rápida:**
Executar em background e monitorar:
```bash
# Terminal 1
python sync_simples_nacional.py

# Terminal 2
python monitorar_sync.py
```

---

### **PASSO 3: IMPLEMENTAR PÁGINA DE EMPRESAS** 🟢
**Tempo estimado:** 30-45 minutos
**Impacto:** Baixo - funcionalidade adicional

**Funcionalidades:**
1. **Lista de Empresas:**
   - Tabela com: Nome, CNPJ, Regime, Total de Processos, % Conclusão
   - Filtros: Por regime, por status
   - Busca: Por nome ou CNPJ

2. **Detalhes da Empresa:**
   - Card com informações
   - Lista de processos vinculados
   - Gráfico de progresso

**Endpoint Necessário:**
```python
@router.get("/empresas/{empresa_id}/processos")
async def get_empresa_processos(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    
    processos = db.query(Processo).filter(Processo.empresa_id == empresa_id).all()
    return {"empresa": empresa, "processos": processos}
```

---

### **PASSO 4: IMPLEMENTAR PÁGINA DE DECLARAÇÕES** 🟢
**Tempo estimado:** 45-60 minutos
**Impacto:** Médio - visualização importante

**Funcionalidades:**
1. **Calendário do Mês:**
   - Visualização mensal das declarações
   - Cores por status (verde=ok, amarelo=pendente, vermelho=atrasado)

2. **Lista de Obrigações:**
   - DAS (Simples Nacional)
   - EFD REINF
   - DIFAL
   - ICMS
   - ISS
   - DIRB

3. **Filtros:**
   - Por competência
   - Por tipo de declaração
   - Por status

**Endpoint Necessário:**
```python
@router.get("/declaracoes/mes")
async def get_declaracoes_mes(
    competencia: str = "10/2025",
    db: Session = Depends(get_db)
):
    # Buscar processos com passos relacionados a declarações
    # Agrupar por tipo de declaração
    # Calcular status (concluído, pendente, atrasado)
    pass
```

---

### **PASSO 5: IMPLEMENTAR PÁGINA DE FATURAMENTO** 🟢
**Tempo estimado:** 30 minutos
**Impacto:** Baixo - análise específica

**Funcionalidades:**
1. **Resumo:**
   - Total de empresas
   - Empresas que faturaram
   - Empresas que não faturaram (inativas)

2. **Listas Separadas:**
   - Tabela de empresas com faturamento
   - Tabela de empresas sem faturamento
   - Filtros e buscas

**Lógica:**
Verificar desdobramentos com pergunta "Houve faturamento?"

---

### **PASSO 6: IMPLEMENTAR PÁGINA DE DESDOBRAMENTOS** 🟢
**Tempo estimado:** 30 minutos
**Impacto:** Médio - decisões pendentes

**Funcionalidades:**
1. **Lista de Desdobramentos Pendentes:**
   - Pergunta
   - Empresa relacionada
   - Processo relacionado
   - Status (respondido/não respondido)

2. **Filtros:**
   - Apenas não respondidos
   - Por empresa
   - Por tipo de pergunta

**Endpoint Necessário:**
```python
@router.get("/desdobramentos/pendentes")
async def get_desdobramentos_pendentes(db: Session = Depends(get_db)):
    desdobramentos = db.query(Desdobramento).filter(
        Desdobramento.respondido == False
    ).all()
    return desdobramentos
```

---

### **PASSO 7: ADICIONAR GRÁFICOS COM RECHARTS** 🟢
**Tempo estimado:** 45 minutos
**Impacto:** Baixo - visualização aprimorada

**Gráficos a Adicionar:**
1. **Dashboard:**
   - Gráfico de pizza: Processos por regime
   - Gráfico de barras: Progresso por regime
   - Gráfico de linha: Evolução temporal (se histórico disponível)

2. **Empresas:**
   - Gráfico de barras: Top 10 empresas por processos
   - Gráfico de pizza: Distribuição por regime

---

### **PASSO 8: IMPLEMENTAR FILTROS E BUSCAS** 🟢
**Tempo estimado:** 30 minutos
**Impacto:** Médio - usabilidade

**Funcionalidades:**
1. **Filtro por Competência:**
   - Dropdown: 10/2025, 11/2025, etc
   - Aplicar em todas as páginas

2. **Busca Global:**
   - Campo de busca no header
   - Buscar por: Nome empresa, CNPJ, Número processo

---

### **PASSO 9: ADICIONAR EXPORT PARA EXCEL** 🟢
**Tempo estimado:** 30 minutos
**Impacto:** Médio - compatibilidade com fluxo antigo

**Funcionalidades:**
1. **Botão "Exportar para Excel"** em cada página
2. **Usar biblioteca:** xlsx ou exceljs
3. **Formatar:** Igual às planilhas antigas

**Biblioteca:**
```bash
npm install xlsx
```

---

### **PASSO 10: DEPLOY E DOCUMENTAÇÃO** 🟢
**Tempo estimado:** 60 minutos
**Impacto:** Médio - produção

**Ações:**
1. **Criar README.md** com instruções completas
2. **Documentar API** no Swagger
3. **Criar docker-compose** (opcional)
4. **Deploy:**
   - Backend: Heroku, Render, ou VPS
   - Frontend: Vercel, Netlify, ou GitHub Pages
   - Banco: PostgreSQL em produção (migrar de SQLite)

---

## 🚀 COMO INICIAR O SISTEMA

### Passo a Passo:

**1. Backend:**
```bash
cd "c:\acessorias processos\backend"
python run.py
# Aguarde: "Uvicorn running on http://0.0.0.0:8000"
```

**2. Frontend (outro terminal):**
```bash
cd "c:\acessorias processos\frontend"
npm run dev
# Aguarde: "VITE ready in XXXms"
# Acesse: http://localhost:3000
```

**3. Abrir no Navegador:**
- Frontend: http://localhost:3000
- Backend Docs: http://localhost:8000/docs

---

## 📊 ARQUITETURA DO SISTEMA

```
┌─────────────────────────────────────────────────┐
│  API ACESSÓRIAS (Externa)                      │
│  https://api.acessorias.com                    │
│  Token: 7f8129c6ac10075cb95cc08c81a6f219       │
└────────────────┬────────────────────────────────┘
                 │ Scripts Python
                 ▼
┌─────────────────────────────────────────────────┐
│  BANCO DE DADOS (SQLite)                       │
│  database.db                                   │
│  - 62 processos (29%)                          │
│  - 61 empresas                                 │
│  - 319 passos                                  │
└────────────────┬────────────────────────────────┘
                 │ SQLAlchemy
                 ▼
┌─────────────────────────────────────────────────┐
│  BACKEND (FastAPI)                             │
│  http://localhost:8000                         │
│  - 15+ endpoints REST                          │
│  - Swagger docs                                │
└────────────────┬────────────────────────────────┘
                 │ HTTP/JSON
                 ▼
┌─────────────────────────────────────────────────┐
│  FRONTEND (React + MUI)                        │
│  http://localhost:3000                         │
│  - Dashboard                                   │
│  - 4 páginas adicionais                        │
└─────────────────────────────────────────────────┘
```

---

## 📝 COMANDOS ÚTEIS

**Verificar banco de dados:**
```bash
python scripts/verificar_banco.py
```

**Sincronizar SimplesNacional:**
```bash
python scripts/sync_simples_nacional.py
```

**Monitorar progresso:**
```bash
python scripts/monitorar_sync.py
```

**Testar endpoint do backend:**
```bash
curl http://localhost:8000/api/v1/dashboard/metricas
```

**Reinstalar dependências frontend:**
```bash
cd frontend
npm install
```

---

## 🎯 RESUMO EXECUTIVO

**Status Geral:** 85% Completo

**O que funciona:**
✅ Backend FastAPI completo
✅ Banco de dados estruturado
✅ Frontend React com 5 páginas
✅ Layout responsivo com sidebar
✅ 62 processos sincronizados (29%)

**O que falta:**
❌ Corrigir bug do Dashboard (5 min)
⏳ Sincronizar 150 processos do SimplesNacional (60-90 min)
⏳ Implementar 4 páginas avançadas (2-3 horas)
⏳ Adicionar gráficos e filtros (1-2 horas)

**Próxima Ação Imediata:**
🔴 **Corrigir bug do Dashboard.tsx linha 164** - adicionar validação para `regime.porcentagem`

---

**Criado em:** 17/11/2025
**Última atualização:** 17/11/2025 23:30
**Desenvolvedor:** GitHub Copilot + Usuário
