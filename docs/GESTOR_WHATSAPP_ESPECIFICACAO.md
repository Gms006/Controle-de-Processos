# 📱 GESTOR DE PROCESSOS CONTÁBEIS VIA WHATSAPP
## Sistema de Gestão Inteligente - 100% Gratuito (Apenas Recebimento)

---

## 🎯 VISÃO GERAL

Sistema de gestão de processos contábeis com interface via **WhatsApp Business API**, permitindo consultas rápidas e análises em tempo real **sem custos de envio de mensagens** (apenas recebimento de comandos do gestor).

### Principais Características:

✅ **100% Gratuito**: Sistema apenas **recebe** comandos (não envia mensagens automáticas)  
✅ **Interface Mobile**: Acesso rápido via WhatsApp de qualquer lugar  
✅ **Análises Robustas**: Métricas gerenciais e operacionais completas  
✅ **Fácil Visualização**: Relatórios formatados com emojis e tabelas  
✅ **Comandos Simples**: Menu intuitivo com números e palavras-chave  

---

## 📊 ANÁLISE DO PROJETO ATUAL

### Dados Disponíveis:

**1. EMPRESAS (211 empresas)**
- 61 empresas cadastradas no banco
- 5 regimes tributários:
  - Simples Nacional (150 processos - 71% do volume)
  - Lucro Presumido Comércio (44 processos)
  - Lucro Presumido Serviços (28 processos)
  - Lucro Real Comércio (17 processos)
  - Lucro Real Serviços (17 processos)

**2. PROCESSOS (211 processos)**
- 62 processos sincronizados (29%)
- 319 passos vinculados
- 136 desdobramentos (perguntas/respostas)
- Competência: 10/2025

**3. MÉTRICAS IDENTIFICADAS:**
- ✅ Taxa de conclusão por regime
- ✅ Dias corridos/tempo de processamento
- ✅ Passos concluídos vs pendentes
- ✅ Desdobramentos respondidos vs pendentes
- ✅ Empresas paradas (0% progresso)
- ✅ Gargalos por tipo de passo

**4. OBRIGAÇÕES ACESSÓRIAS:**
- EFD REINF
- DIRB (apenas Lucro Presumido)
- DIFAL Consumo/Imobilizado
- ISS (Comércio/Indústria/Serviços)
- ICMS (Comércio/Indústria/Serviços)
- EFD Contribuições
- PIS/COFINS
- IRPJ e CSLL
- MIT

---

## 🏗️ ARQUITETURA DO SISTEMA

```
┌─────────────────────────────────────────────────────────────┐
│                    GESTOR (VOCÊ)                            │
│              📱 WhatsApp Business                           │
└─────────────────┬───────────────────────────────────────────┘
                  │ Envia Comando
                  ▼
┌─────────────────────────────────────────────────────────────┐
│          WHATSAPP BUSINESS API (Webhook)                    │
│  • Recebe mensagem via HTTP POST                           │
│  • Extrai comando e telefone do remetente                  │
│  • Autentica gestor (número autorizado)                    │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│          PROCESSADOR DE COMANDOS (Python)                   │
│  • Parseia comando (números ou palavras-chave)             │
│  • Valida permissões                                       │
│  • Roteia para módulo específico                           │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│              MÓDULO DE ANÁLISE (KPIs)                       │
│  • Consulta banco de dados SQLite                          │
│  • Calcula métricas em tempo real                          │
│  • Identifica alertas e gargalos                           │
│  • Gera insights automáticos                               │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│          FORMATADOR DE RELATÓRIOS (WhatsApp)                │
│  • Templates de relatórios                                 │
│  • Formatação com emojis e símbolos                        │
│  • Tabelas otimizadas para mobile                          │
│  • Gráficos ASCII art                                      │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│      RESPOSTA VIA WHATSAPP API (HTTP Response)              │
│  • Envia resposta formatada                                │
│  • Retorna no mesmo contexto da conversa                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📱 MENU PRINCIPAL - COMANDOS DISPONÍVEIS

```
╔════════════════════════════════════╗
║  🤖 GESTOR DE PROCESSOS CONTÁBEIS  ║
║       Competência: 10/2025         ║
╚════════════════════════════════════╝

📊 RESUMOS EXECUTIVOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1️⃣ Resumo Geral (KPIs principais)
2️⃣ Resumo por Regime Tributário
3️⃣ Resumo por Empresa

🔍 ANÁLISES ESPECÍFICAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4️⃣ Empresas sem Faturamento
5️⃣ Empresas com Tributos Apurados
6️⃣ Declarações Pendentes
7️⃣ Declarações Dispensadas

⏱️ DESEMPENHO E PRODUTIVIDADE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
8️⃣ Tempo de Finalização por Empresa
9️⃣ Processos Atrasados/Críticos
🔟 Top 10 Empresas Mais Rápidas
1️⃣1️⃣ Top 10 Empresas Mais Lentas

🚨 ALERTAS E GARGALOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1️⃣2️⃣ Empresas Paradas (0% progresso)
1️⃣3️⃣ Gargalos por Tipo de Passo
1️⃣4️⃣ Desdobramentos Não Respondidos
1️⃣5️⃣ Obrigações Acessórias Pendentes

📈 INDICADORES GERENCIAIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1️⃣6️⃣ Taxa de Conclusão Geral
1️⃣7️⃣ Média de Dias por Regime
1️⃣8️⃣ Análise de Faturamento (REINF)
1️⃣9️⃣ Análise de DIRB/MIT/EFD

🔎 CONSULTAS PERSONALIZADAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2️⃣0️⃣ Buscar por Nome da Empresa
2️⃣1️⃣ Buscar por CNPJ
2️⃣2️⃣ Filtrar por Status

⚙️ CONFIGURAÇÕES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2️⃣3️⃣ Ajuda (Lista de Comandos)
2️⃣4️⃣ Sobre o Sistema

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 Digite o número ou palavra-chave
   Ex: "1" ou "resumo geral"
```

---

## 📊 EXEMPLOS DE RELATÓRIOS

### 1️⃣ RESUMO GERAL

```
╔════════════════════════════════════╗
║     📊 RESUMO GERAL - 10/2025      ║
╚════════════════════════════════════╝

🏢 EMPRESAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 211 empresas
✅ Concluídas: 21 (10.0%)
⏳ Em Andamento: 190 (90.0%)
🛑 Paradas (0%): 35 empresas (16.6%)

📈 PROGRESSO MÉDIO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Geral: ▓▓▓░░░░░░░ 28.5%
Simples Nacional: ▓░░░░░░░░░ 4.0%
Lucro Presumido: ▓▓▓▓▓▓░░░░ 26.8%
Lucro Real: ▓▓▓▓▓▓▓░░░ 50.0%

⏱️ TEMPO MÉDIO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Dias corridos: 15.9 dias
Meta mensal: 30 dias
Status: 🟢 Dentro do prazo

🎯 PASSOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 2.995 passos
✅ Concluídos: 1.039 (34.7%)
⏳ Pendentes: 1.956 (65.3%)

❓ DESDOBRAMENTOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 736 perguntas
✅ Respondidos: 50 (6.8%)
⏳ Pendentes: 686 (93.2%)

🚨 ALERTAS CRÍTICOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 336 empresas aguardando info
   de FATURAMENTO (92% pendente)
   
🔴 338 empresas aguardando info
   de REINF (93% pendente)

🟡 35 empresas paradas há 16 dias
   sem nenhum progresso

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Próximas Ações:
1. Coletar info de faturamento
2. Investigar Simples Nacional
3. Desbloquear empresas paradas
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Digite outro número ou 0 para menu
```

### 2️⃣ RESUMO POR REGIME

```
╔════════════════════════════════════╗
║   📊 ANÁLISE POR REGIME - 10/2025  ║
╚════════════════════════════════════╝

🟢 SIMPLES NACIONAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Empresas: 150 (71.1% do total)
Concluídos: 6 (4.0%) 🔴
Em Andamento: 144 (96.0%)
Dias Médios: 12.5 dias
Status: 🔴 CRÍTICO - Apenas 4% concluído

🔵 LUCRO PRESUMIDO - COMÉRCIO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Empresas: 44 (20.9% do total)
Concluídos: 11 (25.0%) 🟡
Em Andamento: 33 (75.0%)
Dias Médios: 18.2 dias
Status: 🟡 REGULAR

🔵 LUCRO PRESUMIDO - SERVIÇOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Empresas: 28 (13.3% do total)
Concluídos: 8 (28.6%) 🟢
Em Andamento: 20 (71.4%)
Dias Médios: 16.8 dias
Status: 🟢 BOM - Melhor performance

🟣 LUCRO REAL - COMÉRCIO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Empresas: 17 (8.1% do total)
Concluídos: 8 (47.1%) 🟢
Em Andamento: 9 (52.9%)
Dias Médios: 19.5 dias
Status: 🟢 BOM

🟣 LUCRO REAL - SERVIÇOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Empresas: 17 (8.1% do total)
Concluídos: 9 (52.9%) 🟢
Em Andamento: 8 (47.1%)
Dias Médios: 21.3 dias
Status: 🟢 BOM - Maior taxa conclusão

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 Ranking de Desempenho:
1º Lucro Real Serviços (52.9%)
2º Lucro Real Comércio (47.1%)
3º LP Serviços (28.6%)
4º LP Comércio (25.0%)
5º Simples Nacional (4.0%) ⚠️
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Digite outro número ou 0 para menu
```

### 4️⃣ EMPRESAS SEM FATURAMENTO

```
╔════════════════════════════════════╗
║  🔍 EMPRESAS SEM FATURAMENTO       ║
║        Competência: 10/2025        ║
╚════════════════════════════════════╝

📊 VISÃO GERAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Analisado: 211 empresas
Sem Faturamento: 87 empresas (41.2%)
Com Faturamento: 124 empresas (58.8%)

❓ AGUARDANDO RESPOSTA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Desdobramento "Faturamento":
336 empresas pendentes (92.1%)

📋 LISTA - EMPRESAS SEM FATURAMENTO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. MOUSSA CONSTRUTORA LTDA
   CNPJ: 38.135.574/0001-40
   Regime: Simples Nacional
   Status: Dispensado de Declarações
   Dias: 12 dias

2. EXEMPLO COMÉRCIO LTDA
   CNPJ: 11.222.333/0001-44
   Regime: Lucro Presumido Comércio
   Status: Dispensado de Declarações
   Dias: 18 dias

[... lista continua ...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 IMPACTO NO FATURAMENTO:
• 41.2% das empresas sem movimento
• Média de 15.2 dias para identificar
• 336 empresas aguardando confirmação

✅ Ações Recomendadas:
1. Acelerar coleta de info faturamento
2. Validar empresas inativas
3. Dispensar declarações desnecessárias
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Digite outro número ou 0 para menu
```

### 5️⃣ EMPRESAS COM TRIBUTOS APURADOS

```
╔════════════════════════════════════╗
║  💰 EMPRESAS COM TRIBUTOS          ║
║        Competência: 10/2025        ║
╚════════════════════════════════════╝

📊 RESUMO DE APURAÇÃO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total de Empresas: 211
Com Tributos: 124 empresas (58.8%)
Sem Tributos: 87 empresas (41.2%)

💵 TRIBUTOS FEDERAIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PIS/COFINS: 89 empresas
IRPJ: 67 empresas
CSLL: 67 empresas
EFD Contribuições: 78 empresas

🏛️ TRIBUTOS ESTADUAIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ICMS: 56 empresas
DIFAL: 23 empresas

🏙️ TRIBUTOS MUNICIPAIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ISS: 34 empresas

📋 OBRIGAÇÕES ACESSÓRIAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EFD REINF: 338 empresas pendentes
DIRB: 12 empresas (apenas LP)
MIT: 45 empresas (LP e LR)

🎯 TOP 10 - MAIOR CARGA TRIBUTÁRIA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. EMPRESA ABC LTDA (6 tributos)
2. EMPRESA XYZ S/A (6 tributos)
3. EMPRESA DEF LTDA (5 tributos)
[... continua ...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Próximas Ações:
1. Conferir guias geradas (89 empresas)
2. Validar EFD REINF (338 pendentes)
3. Confirmar DIRB obrigatório (12 emp)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Digite outro número ou 0 para menu
```

### 6️⃣ DECLARAÇÕES PENDENTES

```
╔════════════════════════════════════╗
║  📋 DECLARAÇÕES PENDENTES          ║
║        Competência: 10/2025        ║
╚════════════════════════════════════╝

🔴 OBRIGAÇÕES CRÍTICAS (Prazo curto)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DAS - Simples Nacional
📅 Prazo: 20/11/2025 (2 dias)
Empresas: 150
Status: 🔴 6 entregues (4%)
Pendentes: 144 empresas

EFD REINF
📅 Prazo: 15/11/2025 (ATRASADO!)
Empresas: 338
Status: 🔴 0 entregues (0%)
Pendentes: 338 empresas ⚠️

🟡 OBRIGAÇÕES REGULARES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EFD Contribuições
📅 Prazo: 10/12/2025 (22 dias)
Empresas: 78
Status: 🟡 12 entregues (15.4%)
Pendentes: 66 empresas

DIFAL Consumo/Imobilizado
📅 Prazo: 09/12/2025 (21 dias)
Empresas: 23
Status: 🟡 3 entregues (13.0%)
Pendentes: 20 empresas

🟢 OBRIGAÇÕES EM DIA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DIRB (Lucro Presumido)
📅 Prazo: 15/12/2025 (27 dias)
Empresas: 12
Status: 🟢 8 entregues (66.7%)
Pendentes: 4 empresas

MIT (Lucro Presumido/Real)
📅 Prazo: 20/12/2025 (32 dias)
Empresas: 45
Status: 🟢 23 entregues (51.1%)
Pendentes: 22 empresas

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ URGÊNCIAS:
1. 🔴 EFD REINF ATRASADA (338 emp)
2. 🔴 DAS - 2 dias p/ vencimento
3. 🟡 EFD Contribuições - 22 dias
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Digite outro número ou 0 para menu
```

### 8️⃣ TEMPO DE FINALIZAÇÃO POR EMPRESA

```
╔════════════════════════════════════╗
║  ⏱️ TEMPO DE FINALIZAÇÃO           ║
║        Competência: 10/2025        ║
╚════════════════════════════════════╝

📊 ESTATÍSTICAS GERAIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Empresas Concluídas: 21 (10.0%)
Média Geral: 18.3 dias
Mínimo: 8 dias
Máximo: 28 dias
Mediana: 17 dias

📈 POR REGIME TRIBUTÁRIO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Simples Nacional:
  Média: 12.5 dias ✅ RÁPIDO
  Empresas: 6 concluídas

Lucro Presumido Serviços:
  Média: 16.8 dias ✅ BOM
  Empresas: 8 concluídas

Lucro Presumido Comércio:
  Média: 18.2 dias 🟡 REGULAR
  Empresas: 11 concluídas

Lucro Real Comércio:
  Média: 19.5 dias 🟡 REGULAR
  Empresas: 8 concluídas

Lucro Real Serviços:
  Média: 21.3 dias 🟠 LENTO
  Empresas: 9 concluídas

🏆 TOP 5 - MAIS RÁPIDAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. EMPRESA ALPHA LTDA
   Regime: Simples Nacional
   ⏱️ 8 dias | ✅ 100%

2. EMPRESA BETA COMÉRCIO
   Regime: LP Comércio
   ⏱️ 10 dias | ✅ 100%

3. EMPRESA GAMMA SERVIÇOS
   Regime: LP Serviços
   ⏱️ 11 dias | ✅ 100%

[... continua ...]

🐌 TOP 5 - MAIS LENTAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. EMPRESA OMEGA S/A
   Regime: LR Serviços
   ⏱️ 28 dias | ✅ 100%
   Gargalo: Validação REINF

2. EMPRESA DELTA LTDA
   Regime: LR Comércio
   ⏱️ 26 dias | ✅ 100%
   Gargalo: EFD Contribuições

[... continua ...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 Insight:
• Simples Nacional 46% mais rápido
• Lucro Real 38% mais lento
• Gargalo: EFD REINF e Contribuições
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Digite outro número ou 0 para menu
```

### 1️⃣2️⃣ EMPRESAS PARADAS

```
╔════════════════════════════════════╗
║  🛑 EMPRESAS PARADAS (0% progresso)║
║        Competência: 10/2025        ║
╚════════════════════════════════════╝

⚠️ SITUAÇÃO CRÍTICA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total de Empresas Paradas: 35 (16.6%)
Tempo Médio Paradas: 16.0 dias
Impacto: 🔴 ALTO

📋 MOTIVOS DE BLOQUEIO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Aguardando Faturamento: 28 empresas
Aguardando REINF: 4 empresas
Aguardando Documentos: 2 empresas
Outros: 1 empresa

📊 POR REGIME
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Simples Nacional: 22 empresas (62.9%)
LP Comércio: 7 empresas (20.0%)
LP Serviços: 4 empresas (11.4%)
LR: 2 empresas (5.7%)

🔴 LISTA - EMPRESAS PARADAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. MOUSSA CONSTRUTORA LTDA
   CNPJ: 38.135.574/0001-40
   Regime: Simples Nacional
   Parada há: 12 dias
   Bloqueio: Aguardando Faturamento
   Próximo Passo: "Houve Faturamento?"

2. EMPRESA XYZ COMÉRCIO LTDA
   CNPJ: 22.333.444/0001-55
   Regime: LP Comércio
   Parada há: 18 dias
   Bloqueio: Aguardando Info REINF
   Próximo Passo: "Fato Gerador REINF?"

[... lista continua ...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Ações Urgentes:
1. Coletar info de faturamento (28)
2. Validar REINF com empresas (4)
3. Solicitar documentos (2)
4. Liberar processos bloqueados

🎯 Meta: Reduzir para <5% em 7 dias
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Digite outro número ou 0 para menu
```

### 2️⃣0️⃣ BUSCAR POR EMPRESA

```
╔════════════════════════════════════╗
║  🔎 BUSCAR POR EMPRESA             ║
╚════════════════════════════════════╝

Digite o nome da empresa ou CNPJ:

[Usuário digita: "MOUSSA"]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 RESULTADO DA BUSCA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏢 MOUSSA CONSTRUTORA LTDA
CNPJ: 38.135.574/0001-40
Código: 406

📊 PROCESSO ATUAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Processo: Simples Nacional — Mensal
Competência: 10/2025
Regime: Simples Nacional
Status: 🟡 Em andamento
Progresso: ░░░░░░░░░░ 0.0%

⏱️ TEMPO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Início: 05/11/2025
Dias Corridos: 12 dias
Previsão: 25/11/2025 (7 dias)

📌 SITUAÇÃO ATUAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Passo Atual: "Iniciar processos"
Status: 🔴 Pendente
Responsável: João Guimarães

🚧 BLOQUEIOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ Aguardando resposta:
   "Houve Faturamento?"

📋 HISTÓRICO DE PASSOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Iniciar processos - 🔴 Pendente
2. Houve Fato Gerador REINF? - ⏳ Bloqueado
3. Houve Faturamento? - ⏳ Bloqueado

❓ DESDOBRAMENTOS PENDENTES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Houve Fato Gerador REINF?
2. Houve Faturamento?
3. Empresa com ISS devido?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Ação Recomendada:
Contatar empresa para confirmar
faturamento de 10/2025
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Digite outro número ou 0 para menu
```

---

## 🛠️ TECNOLOGIAS E COMPONENTES

### Backend (Python):

**1. WhatsApp Business API**
- **Meta Cloud API** (Gratuito com limitações)
- **Twilio WhatsApp API** (Pago mas robusto)
- **Baileys** (Open source - via Node.js)
- **Evolution API** (Open source - recomendado)

**2. Framework Web**
- **FastAPI** (já implementado)
- Webhook para receber mensagens
- Endpoints para responder

**3. Banco de Dados**
- **SQLite** (já implementado)
- Modelos: Empresa, Processo, Passo, Desdobramento

**4. Módulos Python**
```
whatsapp/
├── __init__.py
├── webhook.py           # Recebe mensagens do WhatsApp
├── processor.py         # Processa comandos
├── formatador.py        # Formata respostas
├── analytics.py         # Calcula KPIs
└── sender.py            # Envia respostas
```

### Fluxo de Dados:

```python
# 1. Receber comando
@app.post("/webhook/whatsapp")
async def webhook(payload: dict):
    mensagem = payload['messages'][0]['text']
    telefone = payload['messages'][0]['from']
    
    # 2. Autenticar
    if not gestor_autorizado(telefone):
        return erro_nao_autorizado()
    
    # 3. Processar comando
    comando = parsear_comando(mensagem)
    
    # 4. Gerar resposta
    resposta = processar_comando(comando)
    
    # 5. Enviar via WhatsApp
    enviar_whatsapp(telefone, resposta)
```

---

## 📊 MÉTRICAS E ANÁLISES DISPONÍVEIS

### 1. MÉTRICAS GERAIS
- Total de empresas
- Taxa de conclusão geral
- Empresas em andamento
- Empresas concluídas
- Empresas paradas (0%)
- Tempo médio de processamento
- Dias corridos máximo/mínimo

### 2. POR REGIME TRIBUTÁRIO
- Simples Nacional
- Lucro Presumido (Comércio/Serviços)
- Lucro Real (Comércio/Serviços)
- Taxa de conclusão por regime
- Tempo médio por regime
- Ranking de desempenho

### 3. ANÁLISE DE FATURAMENTO
- Empresas com faturamento
- Empresas sem faturamento
- Empresas aguardando resposta
- Impacto no processo
- Desdobramentos pendentes

### 4. TRIBUTOS APURADOS
- PIS/COFINS
- IRPJ/CSLL
- ICMS/ISS
- DIFAL
- Empresas por quantidade de tributos

### 5. OBRIGAÇÕES ACESSÓRIAS
- EFD REINF (status/prazo)
- DIRB (status/prazo)
- EFD Contribuições (status/prazo)
- MIT (status/prazo)
- Declarações dispensadas

### 6. DESEMPENHO
- Tempo de finalização por empresa
- Top 10 mais rápidas
- Top 10 mais lentas
- Gargalos identificados
- Passos mais demorados

### 7. ALERTAS
- Processos atrasados
- Prazos próximos do vencimento
- Desdobramentos não respondidos
- Empresas paradas há mais de X dias
- Obrigações críticas

---

## 🔒 SEGURANÇA E AUTENTICAÇÃO

### 1. Autenticação de Gestor
```python
GESTORES_AUTORIZADOS = [
    "+5511999999999",  # Seu número
    "+5511888888888",  # Gestor 2
]

def gestor_autorizado(telefone: str) -> bool:
    return telefone in GESTORES_AUTORIZADOS
```

### 2. Rate Limiting
- Máximo 10 comandos por minuto por usuário
- Proteção contra spam/abuso

### 3. Logs de Auditoria
- Registra todos os comandos executados
- Quem executou, quando, qual comando
- Histórico de consultas

---

## 💰 CUSTOS E LIMITAÇÕES

### WhatsApp Business API - Opções:

**1. Meta Cloud API (GRATUITO)**
- ✅ 1.000 conversas gratuitas/mês
- ✅ Webhook para receber mensagens
- ❌ Limitado a respostas (24h após msg do usuário)
- 💡 **IDEAL para este projeto**

**2. Evolution API (GRATUITO - Open Source)**
- ✅ Totalmente gratuito
- ✅ Self-hosted
- ✅ Sem limitações de conversas
- ❌ Requer servidor próprio
- 💡 **RECOMENDADO para produção**

**3. Twilio WhatsApp (PAGO)**
- ❌ $0.005 por mensagem recebida
- ❌ $0.005 - $0.08 por mensagem enviada
- ✅ Mais robusto e confiável

### Recomendação:
**Evolution API** - Totalmente gratuito, sem custos de envio!

---

## 🚀 PRÓXIMOS PASSOS PARA IMPLEMENTAÇÃO

### Fase 1: Estrutura Base (1-2 dias)
1. Configurar Evolution API ou Meta Cloud API
2. Criar webhook para receber mensagens
3. Implementar autenticação de gestor
4. Criar processador de comandos básico

### Fase 2: Módulo de Análise (2-3 dias)
1. Criar serviço de KPIs e métricas
2. Consultas ao banco de dados
3. Cálculos de estatísticas
4. Identificação de alertas

### Fase 3: Formatação de Relatórios (1-2 dias)
1. Templates de relatórios
2. Formatação WhatsApp (emojis, símbolos)
3. Tabelas otimizadas para mobile
4. Gráficos ASCII

### Fase 4: Comandos Avançados (2-3 dias)
1. Busca por empresa/CNPJ
2. Filtros personalizados
3. Exportação de relatórios
4. Análises comparativas

### Fase 5: Testes e Refinamento (2 dias)
1. Testes de todos os comandos
2. Ajustes de formatação
3. Otimização de performance
4. Documentação final

**TOTAL: 8-12 dias de desenvolvimento**

---

## 📚 DOCUMENTAÇÃO ADICIONAL

Veja também:
- `docs/INSTALACAO_WHATSAPP.md` - Guia de instalação
- `docs/COMANDOS_WHATSAPP.md` - Lista completa de comandos
- `docs/EVOLUTION_API_SETUP.md` - Setup Evolution API
- `backend/whatsapp/README.md` - Documentação técnica

---

## 🎯 BENEFÍCIOS DO SISTEMA

✅ **Mobilidade**: Acesso de qualquer lugar via WhatsApp  
✅ **Velocidade**: Consultas instantâneas (1-3 segundos)  
✅ **Custo Zero**: Sem mensagens automáticas (só recebe)  
✅ **Simplicidade**: Interface familiar (WhatsApp)  
✅ **Insights**: Métricas e análises profundas  
✅ **Alertas**: Identificação proativa de problemas  
✅ **Produtividade**: Decisões rápidas baseadas em dados  

---

**Última atualização:** 18/11/2025  
**Versão:** 1.0  
**Status:** Especificação Completa ✅
