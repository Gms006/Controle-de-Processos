# 🤖 INSTRUÇÕES PARA O PRÓXIMO AGENTE
## Sistema de Gestão de Processos Contábeis

---

## 📍 CONTEXTO ATUAL

Você está trabalhando em um sistema web de gestão de processos contábeis.
O projeto está **85% completo** mas tem **1 bug crítico** que impede o funcionamento.

**Servidores Rodando:**
- ✅ Backend: http://localhost:8000 (FastAPI)
- ✅ Frontend: http://localhost:3000 (React)

**Estrutura:**
```
c:\acessorias processos\
├── backend/          # FastAPI + SQLite (funcionando)
├── frontend/         # React + MUI (bug no Dashboard)
├── scripts/          # Sincronização com API
├── database.db       # 62/211 processos (29%)
└── RESUMO_PROJETO.md # Leia este arquivo PRIMEIRO
```

---

## 🔴 TAREFA CRÍTICA #1: CORRIGIR BUG DO DASHBOARD

**Problema:**
Dashboard.tsx quebra na linha 164 com erro:
```
TypeError: Cannot read properties of undefined (reading 'toFixed')
```

**Arquivo:** `c:\acessorias processos\frontend\src\pages\Dashboard.tsx`
**Linha:** 164

**Causa:**
O backend retorna dados em `por_regime` mas o campo `porcentagem` vem como `undefined`.

**Solução Rápida (Frontend):**
Localizar linha 164 e trocar:
```typescript
// ANTES (linha ~221):
{regime.porcentagem.toFixed(1)}%

// DEPOIS:
{(regime.porcentagem ?? 0).toFixed(1)}%
```

**OU Solução Definitiva (Backend):**
Arquivo: `c:\acessorias processos\backend\app\routers\dashboard.py`

Localizar função `get_metricas()` e adicionar cálculo de porcentagem:
```python
por_regime.append({
    "regime": regime,
    "total": total,
    "concluidos": concluidos,
    "porcentagem": (concluidos / total * 100) if total > 0 else 0  # ← ADICIONAR
})
```

**Teste:**
1. Reiniciar backend (se alterou backend)
2. Atualizar página: http://localhost:3000
3. Dashboard deve aparecer completo com métricas

---

## 🟡 TAREFA #2: VERIFICAR DADOS NO BANCO

**Objetivo:** Confirmar quantos processos existem e quais regimes.

**Comando:**
```bash
cd "c:\acessorias processos"
python scripts/verificar_banco.py
```

**Saída Esperada:**
```
📊 Total de processos: 62

📋 Por regime:
   LucroPresumido: 44 empresas
   LucroReal: 17 empresas
```

**Se SimplesNacional = 0:**
- Normal! Falta sincronizar 150 processos do SimplesNacional
- Não é crítico para o funcionamento do dashboard
- Pode ser feito depois

---

## 🟢 TAREFA #3: TESTAR DASHBOARD COMPLETO

**Após corrigir o bug, verificar se aparece:**

✅ **Header:** "Dashboard" + Botão "Atualizar"
✅ **4 Cards:**
- Total: 62 processos
- Concluídos: X (com %)
- Em Andamento: Y
- Empresas: 61

✅ **Seção "Processos por Regime":**
- LucroPresumido: Barra de progresso
- LucroReal: Barra de progresso

**Se tudo aparecer corretamente:**
✅ Bug corrigido com sucesso!

---

## 📋 PRÓXIMAS TAREFAS (ORDEM DE PRIORIDADE)

### TAREFA #4: Implementar Página de Empresas

**Arquivo:** `c:\acessorias processos\frontend\src\pages\Empresas.tsx`

**Funcionalidades:**
1. Tabela com lista de empresas
2. Colunas: Nome, CNPJ, Regime, Processos, % Conclusão
3. Filtro por regime
4. Busca por nome/CNPJ

**Endpoint Disponível:**
```
GET http://localhost:8000/api/v1/empresas
```

**Código Base:**
```typescript
import { useEffect, useState } from 'react';
import { Table, TableBody, TableCell, TableHead, TableRow } from '@mui/material';
import axios from 'axios';

export default function Empresas() {
  const [empresas, setEmpresas] = useState([]);
  
  useEffect(() => {
    axios.get('http://localhost:8000/api/v1/empresas')
      .then(res => setEmpresas(res.data))
      .catch(err => console.error(err));
  }, []);
  
  return (
    <Table>
      <TableHead>
        <TableRow>
          <TableCell>Nome</TableCell>
          <TableCell>CNPJ</TableCell>
          <TableCell>Regime</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {empresas.map(emp => (
          <TableRow key={emp.id}>
            <TableCell>{emp.nome}</TableCell>
            <TableCell>{emp.cnpj}</TableCell>
            <TableCell>{emp.regime_tributario}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
```

---

### TAREFA #5: Implementar Página de Declarações

**Arquivo:** `c:\acessorias processos\frontend\src\pages\Declaracoes.tsx`

**Funcionalidades:**
1. Lista de obrigações mensais
2. Cards para cada tipo: DAS, EFD REINF, DIFAL, ICMS, ISS, DIRB
3. Status de cada obrigação (concluída/pendente)

**Endpoint a Criar:**
```python
# backend/app/routers/declaracoes.py
@router.get("/declaracoes/mes")
async def get_declaracoes_mes(competencia: str = "10/2025"):
    # Implementar lógica
    pass
```

---

### TAREFA #6: Completar Sincronização SimplesNacional

**Objetivo:** Adicionar os 150 processos restantes ao banco.

**Comando:**
```bash
cd "c:\acessorias processos\scripts"
python sync_simples_nacional.py
```

**Tempo:** 60-90 minutos (rate limiting da API)

**Monitorar Progresso:**
```bash
# Em outro terminal
python monitorar_sync.py
```

**Não é urgente!** O sistema funciona com os 62 processos atuais.

---

## 🛠️ COMANDOS ÚTEIS

**Iniciar Backend:**
```bash
cd "c:\acessorias processos\backend"
python run.py
```

**Iniciar Frontend:**
```bash
cd "c:\acessorias processos\frontend"
npm run dev
```

**Verificar Banco:**
```bash
python scripts/verificar_banco.py
```

**Ver Logs do Frontend:**
- Pressione F12 no navegador
- Aba "Console"

**Testar Endpoint:**
```bash
curl http://localhost:8000/api/v1/dashboard/metricas
```

---

## ❗ PROBLEMAS COMUNS

**1. "Tela branca no frontend"**
- Causa: Bug na linha 164 do Dashboard.tsx
- Solução: Aplicar TAREFA #1

**2. "Backend não responde"**
- Verificar se está rodando: `curl http://localhost:8000/health`
- Reiniciar: `python backend/run.py`

**3. "npm install falha"**
- Navegar: `cd "c:\acessorias processos\frontend"`
- Reinstalar: `npm install`

**4. "Erro de CORS"**
- Já configurado no backend
- Proxy configurado no vite.config.ts
- Não deve ocorrer

---

## 📚 DOCUMENTAÇÃO DE REFERÊNCIA

**Leia PRIMEIRO:**
1. `RESUMO_PROJETO.md` - Visão geral completa
2. `frontend/README.md` - Documentação do frontend
3. `backend/app/main.py` - Endpoints disponíveis

**Swagger API:**
http://localhost:8000/docs

**Estrutura do Banco:**
```sql
empresas (id, nome, cnpj, regime_tributario, ativa)
processos (id, empresa_id, nome, competencia, status, porcentagem_conclusao)
passos (id, processo_id, ordem, nome, concluido)
desdobramentos (id, processo_id, passo_id, pergunta, resposta, respondido)
sincronizacoes (id, tipo, status, total_processos, criado_em)
```

---

## ✅ CHECKLIST DE VERIFICAÇÃO

Antes de marcar como "concluído", confirme:

**Bug Corrigido:**
- [ ] Dashboard abre sem erros
- [ ] 4 cards aparecem com números
- [ ] Barras de progresso aparecem
- [ ] Botão "Atualizar" funciona

**Navegação:**
- [ ] Sidebar abre/fecha no mobile
- [ ] Clicar em "Empresas" abre página
- [ ] Clicar em "Declarações" abre página
- [ ] Clicar em "Faturamento" abre página
- [ ] Clicar em "Desdobramentos" abre página

**Backend:**
- [ ] Swagger abre em /docs
- [ ] Endpoint /dashboard/metricas retorna dados
- [ ] Endpoint /empresas retorna lista

---

## 🎯 OBJETIVO FINAL

Sistema web completo com:
1. ✅ Dashboard funcional com métricas reais
2. ⏳ 5 páginas implementadas (1 ok, 4 pendentes)
3. ⏳ Banco completo (62/211 processos)
4. ✅ Backend FastAPI robusto
5. ⏳ Gráficos e filtros

**Prioridade Máxima:** Corrigir bug do Dashboard primeiro!

---

**Data:** 17/11/2025 23:30
**Status:** Bug crítico identificado, solução documentada
**Ação Imediata:** Aplicar fix na linha 164 do Dashboard.tsx
