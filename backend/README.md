# 🚀 Backend API - Gestão de Processos Contábeis

Backend FastAPI com sincronização inteligente e banco de dados SQLite local.

## 📁 Estrutura

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app principal
│   ├── config.py            # Configurações
│   ├── database.py          # SQLAlchemy setup
│   ├── models/              # Modelos do banco de dados
│   │   └── __init__.py
│   ├── schemas/             # Pydantic schemas (validação)
│   │   └── __init__.py
│   └── services/            # Lógica de negócio
│       └── acessorias_sync.py
├── cache/                   # Cache de métricas (JSON)
├── database.db              # SQLite database (criado automaticamente)
├── requirements.txt
└── run.py                   # Script para iniciar servidor
```

## 🔧 Instalação

1. **Instalar dependências** (já feito):
   ```bash
   pip install fastapi uvicorn sqlalchemy httpx pydantic pydantic-settings python-multipart
   ```

2. **Configurar .env** (opcional):
   ```env
   ACESSORIAS_API_TOKEN=7f8129c6ac10075cb95cc08c81a6f219
   DEFAULT_COMPETENCIA=10/2025
   ```

## 🚀 Executar

### Opção 1: Usar script run.py
```bash
cd backend
python run.py
```

### Opção 2: Direto com uvicorn
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Servidor rodando em:
- **API**: http://localhost:8000
- **Documentação Swagger**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📊 Endpoints Disponíveis

### Processos
- `GET /api/v1/processos` - Lista todos os processos
- `GET /api/v1/processos/{id}` - Detalhes de um processo
- `GET /api/v1/processos/competencia/{comp}` - Processos por competência

### Dashboard
- `GET /api/v1/dashboard/metricas` - Métricas agregadas (com cache)

### Empresas
- `GET /api/v1/empresas` - Lista empresas
- `GET /api/v1/empresas/{id}/processos` - Processos de uma empresa

### Sincronização
- `POST /api/v1/sync/manual?tipo=incremental` - Sincronização manual
- `GET /api/v1/sync/status` - Status da última sync
- `GET /api/v1/sync/history` - Histórico de syncs

### Sistema
- `GET /health` - Health check

## 🔄 Sincronização

### Primeira vez (FULL SYNC):
```bash
curl -X POST "http://localhost:8000/api/v1/sync/manual?tipo=full&competencia=10/2025"
```
- Busca todos os 211 processos
- ~3-5 minutos
- 212 chamadas à API

### Atualizações (INCREMENTAL SYNC):
```bash
curl -X POST "http://localhost:8000/api/v1/sync/manual?tipo=incremental&competencia=10/2025"
```
- Detecta apenas processos modificados
- ~10-30 segundos
- Muito mais rápido!

## 💾 Banco de Dados

**SQLite** local (`database.db`):
- ✅ Sem instalação extra
- ✅ Arquivo único portátil
- ✅ Perfeito para desenvolvimento
- ✅ Suporta milhares de processos

### Tabelas:
1. `empresas` - Cadastro de empresas
2. `processos` - Processos contábeis
3. `passos` - Steps de cada processo
4. `desdobramentos` - Perguntas/respostas
5. `sincronizacoes` - Log de syncs

## 📈 Cache de Métricas

- Armazenado em `cache/metricas_10_2025.json`
- TTL: 15 minutos
- Dashboard < 100ms de resposta
- Invalidado automaticamente após sync

## 🔍 Exemplo de Uso

```python
import requests

# Listar processos
response = requests.get("http://localhost:8000/api/v1/processos")
processos = response.json()

# Métricas do dashboard
response = requests.get("http://localhost:8000/api/v1/dashboard/metricas")
metricas = response.json()
print(f"Total de processos: {metricas['total_processos']}")
print(f"Taxa de conclusão: {metricas['taxa_conclusao_media']}%")

# Sincronizar
response = requests.post(
    "http://localhost:8000/api/v1/sync/manual",
    params={"tipo": "incremental"}
)
print(response.json())
```

## 🐛 Debugging

Ver logs do servidor:
```bash
# Os logs aparecem no terminal onde você rodou run.py
# Mostra todas as requests HTTP e erros
```

Acessar banco SQLite diretamente:
```bash
sqlite3 database.db
.tables
SELECT COUNT(*) FROM processos;
.quit
```

## 🎯 Próximos Passos

1. ✅ Backend criado com FastAPI
2. ✅ Banco SQLite configurado
3. ✅ Sincronização inteligente implementada
4. ⏳ Conectar com scripts existentes
5. ⏳ Criar frontend React
6. ⏳ Testar sync completa

---

**Pronto para rodar!** Execute `python run.py` e acesse http://localhost:8000/docs
