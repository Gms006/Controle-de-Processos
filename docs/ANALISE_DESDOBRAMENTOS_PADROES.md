# 📊 ANÁLISE COMPLETA DE DESDOBRAMENTOS E PADRÕES
## Baseado em Screenshots do Sistema Acessórias

---

## 🔍 PADRÕES IDENTIFICADOS NOS SCREENSHOTS

### SCREENSHOT 1: Estrutura Geral de Desdobramentos

**Desdobramento 1: Empresa obrigada a DIRB?**
- Tipo: Desdobramento
- Alternativas: Não / Sim
- Se **Não** → Conclui o passo
- Se **Sim** → Obrigatoriedade do DIRB

**Desdobramento 2: Houve Fato Gerador para entrega da EFD REINF?**
- Tipo: Desdobramento
- Alternativas: Sim / Não
- Se **Sim** → Gerar Obrigação - REINF
- Se **Não** → Dispensa de Entrega - EFD REINF

**Desdobramento 3: Houve Faturamento?**
- Tipo: Desdobramento
- Alternativas: Sim / Não / Não, Mas houve faturamento no trimestre / Sem faturamento no mês, mas com IRP/CSLL devidos no trimestre
- Se **Sim** → Acompanhamento Mensal (Comércio, Indústria e Serviços)
- Se **Não** → Dispensa da entrega das declarações

**Passo Simples: Concluir apuração Mensal**
- Apenas selecione "Joinha" para finalizar

**Follow-Up (2x):**
- Controle mensal - Disparado por e-mail específico

---

### SCREENSHOT 2: Matriz DIRB (Obrigatoriedade do DIRB)

**Nome da Matriz**: Obrigatoriedade do DIRB
**Departamento**: Fiscal
**Barra vermelha**: 20 dias
**Só sub-matriz**: Sim
**Pede autorização**: Não

**Estrutura:**
1. **Passo simples**: Obrigatoriedade do DIRB
   - Cria obrigação DIRB após o início/autorização do processo
   
2. **Follow-Up (3x)**: DIRB - obrigação de entrega confirmada
   - Disparado para e-mails específicos (Marco, João Guimarães, Fernando)

**Matrizes que utilizam**: 
- Lucro Presumido - Comércio e Indústria
- Lucro Presumido - Comércio, Indústria e Serviços

---

### SCREENSHOT 3: Matriz Comércio/Indústria/Serviços (COMPLETA)

**Passo 1**: Coleta das documentações e importação dos documentos fiscais no sistema
- Dica: Importar NFe/NFCe/CTe/serviços, conferir lotes e rejeições
- Validar: CFOP/CSOSN/CST e CFOP interessadual

**Desdobramento 1**: Houve compra de consumo/imobilizado fora do estado?
- Sim → DIFAL Consumo/Imobilizado
- Não → Conclui o passo

**Desdobramento 2**: Empresa com ISS devido?
- Não → Conclui o passo
- Sim → Empresa com Incidência de ISS

**Desdobramento 3**: Empresa com ICMS devido?
- Não → Conclui o passo
- Sim → Empresa com Incidência de ICMS

**Desdobramento 4**: Houve incidência de Tributos Federais?
- Sim → EFD Contribuições obrigatoriedade
- Não → Conclui o passo
- Empresa isenta de tributos Federais → Obrigação de entrega - EFD Contribuições

**Passo simples**: Guia de PIS/COFINS (cumulativo) entregue ao cliente
- Se não houve cobrança, dispense o processo

**Desdobramento 5**: Houve incidência de IRPJ e CSLL?
- Sim → Apuração de IRPJ e CSLL
- Não → Conclui o passo

**Desdobramento 6**: Houve o preenchimento da MIT?
- Sim → MIT preenchida
- Não → Dispensa — MIT
- Sim, mas sem movimento → Confirmar obrigatoriedade de entrega do MIT sem movimento

---

### SCREENSHOT 4: Matriz DIFAL Consumo/Imobilizado

**Passo 1**: Apurar e entregar DIFAL
- Cria obrigação DIFAL Consumo - Regime Normal após o início/autorização do processo

**Passo 2**: DIFAL Consumo - Obrigação gerada
- Obrigação gerada, valide a informação (não há necessidade de anexar a guia)

**Follow-Up (3x)**: DIFAL - Consumo/Imobilizado OBRIGATÓRIO
- Disparado para e-mails específicos (João Guimarães, Joyce, Marco)

**Matrizes que utilizam**:
- Acompanhamento Mensal (Comércio e Indústria)
- Acompanhamento Mensal (Comércio, Indústria e Serviços)
- Acompanhamento Mensal - Serviços

---

### SCREENSHOT 5: Empresa com Incidência de ISS

**Passo 1**: Houve incidência de ISS?
- Confirme se há incidência de ISS

**Passo 2**: Guia de ISS entregue ao cliente
- Se não houve cobrança, dispense o processo

**Matriz que utiliza**:
- Acompanhamento Mensal (Comércio, Indústria e Serviços)

---

### SCREENSHOT 6: Empresa com Incidência de ICMS

**Passo 1**: Empresa com ICMS devido
- Confirme se há incidência de ICMS

**Passo 2**: Guia de ICMS entregue ao cliente
- Se não houve cobrança, dispense o processo

**Matriz que utiliza**:
- Acompanhamento Mensal (Comércio, Indústria e Serviços)

---

## 🎯 PADRÕES IDENTIFICADOS

### 1. ESTRUTURA DE DECISÃO PADRÃO:

```
DESDOBRAMENTO (Pergunta)
  ├── Alternativa 1 → Ação A (Sub-matriz / Passo / Dispensar)
  ├── Alternativa 2 → Ação B
  └── Alternativa 3 (opcional) → Ação C
```

### 2. TIPOS DE AÇÕES:

- **Sub-matriz**: Inicia novo fluxo de processos
- **Passo simples**: Executar e concluir
- **Follow-Up**: E-mail automático para responsável
- **Dispensar**: Encerra sem obrigação

### 3. DESDOBRAMENTOS COMUNS (Todos os Regimes):

1. **DIRB** (apenas Lucro Presumido)
   - Pergunta: "Empresa obrigada a DIRB?"
   - Impacto: Se SIM → cria obrigação + 3 follow-ups

2. **EFD REINF** (todos os regimes)
   - Pergunta: "Houve Fato Gerador para entrega da EFD REINF?"
   - Impacto: Se SIM → Gerar Obrigação, Se NÃO → Dispensar

3. **FATURAMENTO** (todos os regimes)
   - Pergunta: "Houve Faturamento?" ou "Houve faturamento no mês?"
   - Impacto: Define se precisa processar obrigações mensais

4. **DIFAL Consumo/Imobilizado**
   - Pergunta: "Houve compra de consumo/imobilizado fora do estado?"
   - Impacto: Se SIM → gera obrigação DIFAL

5. **ISS** (Comércio/Indústria/Serviços)
   - Pergunta: "Empresa com ISS devido?"
   - Impacto: Se SIM → gera guia ISS

6. **ICMS** (Comércio/Indústria/Serviços)
   - Pergunta: "Empresa com ICMS devido?"
   - Impacto: Se SIM → gera guia ICMS

7. **Tributos Federais** (Lucro Real/Presumido)
   - Pergunta: "Houve incidência de Tributos Federais?"
   - Impacto: Se SIM → EFD Contribuições obrigatória

8. **IRPJ e CSLL** (Lucro Real/Presumido)
   - Pergunta: "Houve incidência de IRPJ e CSLL?"
   - Impacto: Se SIM → apuração obrigatória

9. **MIT** (Lucro Real/Presumido)
   - Pergunta: "Houve o preenchimento da MIT?"
   - Impacto: Confirmar obrigatoriedade

### 4. FOLLOW-UPS:

- **Sempre 3 e-mails diferentes** (Marco, João Guimarães, Joyce, Fernando)
- Disparam após conclusão de passos críticos
- Servem para **notificar responsáveis** sobre obrigações geradas

### 5. BARRAS VERMELHAS (Prazos):

- **DIRB**: 20 dias
- **DIFAL**: 30 dias
- **ISS**: 25 dias
- **ICMS**: 0 dias (imediato)
- **Geral**: 20 dias (padrão)

---

## 🎯 MAPEAMENTO DE OBRIGAÇÕES POR REGIME

### SIMPLES NACIONAL:
1. ✅ DAS (Documento de Arrecadação Simples)
2. ✅ EFD REINF (se houver fato gerador)
3. ✅ DIFAL Consumo/Imobilizado (se houver compra fora do estado)
4. ✅ ICMS (se ultrapassar 3.6K)
5. ✅ ISS (se ultrapassar 3.6K)

### LUCRO PRESUMIDO (Serviços/Comércio):
1. ✅ EFD REINF
2. ✅ EFD PIS e COFINS (Contribuições)
3. ✅ MIT (Movimentação de Isentos e Tributados)
4. ✅ DIFAL Consumo (se houver)
5. ✅ IRPJ (Imposto de Renda Pessoa Jurídica)
6. ✅ CSLL (Contribuição Social sobre Lucro Líquido)
7. ✅ ICMS
8. ✅ DIRB (se houver benefícios ou isenções federais)
9. ✅ ISS (se houver serviços)

### LUCRO REAL (Serviços/Comércio):
- **Idêntico ao Lucro Presumido** (mesmas 9 obrigações)

---

## 🔍 ANÁLISE DE PRIORIDADES

### ALTA PRIORIDADE (Bloqueiam Processo):

1. **FATURAMENTO** (361 empresas aguardando)
   - Se NÃO → Dispensa maioria das obrigações
   - Se SIM → Libera fluxo completo
   - **Impacto**: 93% dos processos bloqueados

2. **EFD REINF** (361 empresas aguardando)
   - Pergunta binária: SIM/NÃO
   - **Padrão**: Maioria responde NÃO (dispensar)
   - **Impacto**: Crítico para todos os regimes

3. **DIFAL** (pequeno volume, mas bloqueante)
   - Apenas Lucro Presumido/Real
   - **Padrão**: Maioria responde NÃO
   - **Impacto**: Se SIM → abre sub-matriz com 30 dias

### MÉDIA PRIORIDADE (Dependem de Faturamento):

4. **ICMS/ISS** (após confirmar faturamento)
   - Só aparecem se houver faturamento
   - Simples Nacional: >3.6K
   
5. **Tributos Federais** (EFD Contribuições)
   - Lucro Presumido/Real apenas
   - Depende de faturamento

6. **IRPJ/CSLL**
   - Lucro Presumido/Real apenas
   - Depende de faturamento

### BAIXA PRIORIDADE (Finais):

7. **MIT** (última obrigação)
   - Apenas Lucro Presumido/Real
   - Geralmente SIM ou dispensa

8. **DIRB** (pequeno volume)
   - Apenas Lucro Presumido
   - Apenas 14 empresas questionadas

---

## 💡 INSIGHTS E RECOMENDAÇÕES

### 1. AUTOMAÇÃO POSSÍVEL:

**90% dos desdobramentos seguem 2 padrões:**

**Padrão A - Binário Simples (SIM/NÃO):**
```python
if resposta == "NÃO":
    acao = "Dispensar obrigação"
elif resposta == "SIM":
    acao = "Gerar obrigação + follow-ups"
```

**Padrão B - Múltipla Escolha:**
```python
if resposta == "Sim":
    acao = "Processar obrigação completa"
elif resposta == "Não":
    acao = "Dispensar"
elif resposta == "Não, mas...":
    acao = "Processar parcial"
```

### 2. ORDEM IDEAL DE PROCESSAMENTO:

```
1º FATURAMENTO (desbloqueia 80% das decisões)
   ↓
2º REINF (obrigatório para todos)
   ↓
3º DIFAL (se aplicável - LP/LR)
   ↓
4º ICMS/ISS (se faturamento > 3.6K ou obrigatório)
   ↓
5º EFD Contribuições (LP/LR)
   ↓
6º IRPJ/CSLL (LP/LR)
   ↓
7º MIT (LP/LR - último)
   ↓
8º DIRB (se aplicável)
```

### 3. REGRAS DE NEGÓCIO AUTOMATIZÁVEIS:

**Simples Nacional:**
- Se faturamento = NÃO → Dispensar TUDO exceto DAS
- Se faturamento = SIM + valor < 3.6K → DAS + REINF apenas
- Se faturamento = SIM + valor > 3.6K → DAS + REINF + ICMS/ISS

**Lucro Presumido/Real:**
- Se faturamento = NÃO → Apenas REINF + MIT
- Se faturamento = SIM → Processar TODAS obrigações

### 4. DADOS PARA CAPTURAR NA API:

```python
{
    "competencia": "10/2025",  # Sempre mês anterior
    "faturamento": True/False,
    "valor_faturamento": 15000.00,
    "reinf": True/False,
    "difal": True/False,
    "dirb": True/False,
    "icms": True/False,
    "iss": True/False,
    "tributos_federais": True/False,
    "irpj_csll": True/False,
    "mit": True/False
}
```

---

## 📊 ESTRUTURA IDEAL DO SISTEMA

### FASE 1: CAPTURA DE DADOS (WhatsApp)

**Conversa Inicial:**
```
🤖 Olá! Vamos processar a competência 10/2025

Qual empresa deseja processar?
1️⃣ TINAZO AGRONEGOCIOS LTDA
2️⃣ RADIAL CONSIGNACOES LTDA
...
ou digite o nome
```

**Fluxo de Perguntas (Ordem Inteligente):**
```
Empresa: TINAZO AGRONEGOCIOS LTDA
Regime: Lucro Presumido - Comércio

━━━━━━━━━━━━━━━━━━━━━━━━
📊 DESDOBRAMENTOS OBRIGATÓRIOS
━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣ Houve faturamento no mês?
   • Sim
   • Não
   • Não, mas houve no trimestre

[Aguardando resposta...]
```

### FASE 2: DASHBOARD WEB

**Tela Principal:**
```
┌─────────────────────────────────────────┐
│  📊 GESTÃO DE PROCESSOS - 10/2025       │
└─────────────────────────────────────────┘

🎯 VISÃO GERAL
  211 Empresas | 21 Concluídas (10%)
  
🚨 PENDÊNCIAS CRÍTICAS
  ⚠️ 686 desdobramentos aguardando
  ⚠️ 35 empresas paradas (0%)
  
📋 POR REGIME
  • Simples Nacional: 150 (4% concluído)
  • Lucro Presumido S: 28 (28.6%)
  • Lucro Presumido C: 16 (25%)
  • Lucro Real C: 15 (13.3%)
  • Lucro Real S: 2 (50%)
  
🎯 AÇÕES RÁPIDAS
  [Processar Lote] [Ver Alertas] [Relatórios]
```

---

## 🚀 PRÓXIMOS PASSOS

1. ✅ Analisar desdobramentos na planilha atual
2. ✅ Criar mapeamento completo de padrões
3. ⏳ Desenvolver bot WhatsApp interativo
4. ⏳ Criar dashboard web responsivo
5. ⏳ Implementar regras de automação
6. ⏳ Sistema de notificações (follow-ups)

---

**Competência Identificada**: 10/2025 ✅
**Token WhatsApp**: Confirmado ✅
**Opção Escolhida**: Híbrido WhatsApp + Site ✅
**Equipe**: Múltiplos usuários futuros ✅
