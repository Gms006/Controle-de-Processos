# Estrutura do Processo: Simples Nacional - Mensal

## 📋 Visão Geral

Este documento detalha a estrutura completa do ecossistema de processos "Simples Nacional" conforme implementado no sistema Acessórias.

**Departamento Principal:** Fiscal  
**Complexidade:** Alta (múltiplos desdobramentos)  
**Tipo:** Processo recorrente mensal

---

## 🌳 Matrizes de Processos Identificadas

O Simples Nacional possui **12 matrizes de processos diferentes**, cada uma ativada conforme cenários específicos:

### 1️⃣ **Simples Nacional - Mensal** (Principal)
**Uso:** Processo padrão mensal  
**Departamento:** Fiscal  
**Passos:**
- Passo simples: Validar importações & Conferência de Documentos
- Passo simples: Apuração e Transmissão do PGDAS
- Passo simples: DAS - Validação de Entregas (Acessória)
- **Desdobramento:** Houve DIFAL na competência?
  - **Sim** → Aciona "Tipo de DIFAL"
  - **Não** → Conclui o passo

### 2️⃣ **Simples Nacional - Sem Faturamento**
**Uso:** Empresas sem movimento no mês  
**Departamento:** Fiscal  
**Passos:**
- Passo simples: SN Sem Faturamento (Declaração Zerada)
- 3x Follow-up: Notificações para e-mails específicos

### 3️⃣ **Simples Nacional Com Movimento**
**Uso:** Empresas com faturamento no período  
**Departamento:** Fiscal  
**Passos:**
- **Desdobramento:** KEA ultrapassou o limite estadual de 3.6?
  - **Sim** → Recolhimento do ISS por fora da DAS
  - **Não** → Conclui o passo
- Passo simples: Validar importações & Conferência de Documentos
- Passo simples: Apuração e Transmissão do PGDAS
- Passo simples: DAS - Validação de Entregas (Acessória)
- **Desdobramento:** Houve DIFAL na competência?
  - **Sim** → "Tipo de DIFAL"
  - **Não** → Conclui processo

### 4️⃣ **Gerar Obrigações - REINF**
**Uso:** Verificação de necessidade de REINF  
**Departamento:** Fiscal  
**Passos:**
- Passo simples: Gerar REINF
- **Desdobramento:** Houve Fato Gerador para envios da EFD REINF?
  - **Sim** → Gerar Obrigações REINF
  - **Não** → Dispensa de Entrega - EFD REINF

### 5️⃣ **Dispensa de Entrega - EFD REINF**
**Uso:** Quando não há fatos geradores REINF  
**Departamento:** Fiscal  
**Passos:**
- Passo simples: Empresa Dispensada de Entrega?
- 3x Follow-up: EFD Reinf OBRIGATÓRIA para diferentes destinatários

### 6️⃣ **Recolhimento de ISS por fora da DAS**
**Uso:** Quando ISS é pago separadamente  
**Departamento:** Fiscal  
**Passos:**
- Passo simples: ISS pago fora da DAS
- 3x Follow-up: Notificações para diferentes e-mails específicos

### 7️⃣ **Recolhimento de ICMS por fora da DAS**
**Uso:** Quando ICMS é pago separadamente  
**Departamento:** Fiscal  
**Passos:**
- Passo simples: Confirmar recolhimento de ICMS por fora
- 3x Follow-up: Notificações

### 8️⃣ **Recolhimento de ICMS e ISS por fora da DAS**
**Uso:** Quando ambos tributos são pagos separadamente  
**Departamento:** Fiscal  
**Passos:**
- Passo simples: Confirmar recolhimentos de ICMS e ISS por fora
- 3x Follow-up: Notificações

### 9️⃣ **Tipo de DIFAL**
**Uso:** Classificação do tipo de diferencial de alíquota  
**Departamento:** Fiscal  
**Passos:**
- **Desdobramento:** Tipo de DIFAL
  - **Comercialização** → DIFAL, Comercialização
  - **Consumo/Imobilizado** → DIFAL, Consumo/Imobilizado - Simples Nacional
  - **Ambos** → DIFAL - Comercialização e Consumo/Imobilizado

### 🔟 **DIFAL, Comercialização**
**Uso:** Tratamento de DIFAL por comercialização  
**Departamento:** Fiscal  
**Passos:**
- Passo simples: Incidência da DIFAL, Comercialização
- 3x Follow-up: Notificações

### 1️⃣1️⃣ **DIFAL, Consumo/Imobilizado - Simples Nacional**
**Uso:** Tratamento de DIFAL por consumo/imobilizado  
**Departamento:** Fiscal  
**Passos:**
- Passo simples: Confirmar obrigatoriedade da DIFAL
- 3x Follow-up: Notificações (incluindo disparo manual)

### 1️⃣2️⃣ **DIFAL - Comercialização e Consumo/Imobilizado**
**Uso:** Ambos tipos de DIFAL presentes  
**Departamento:** Fiscal  
**Passos:**
- Passo simples: Incidência da DIFAL de consumo e Comercialização
- 3x Follow-up: Notificações

---

## 🔄 Fluxo de Decisões (Desdobramentos)

### **Árvore de Decisão Principal:**

```
Simples Nacional - Mensal
│
├─ Validar importações & Conferência
├─ Apuração e Transmissão PGDAS
├─ DAS - Validação de Entregas
│
└─ [DESDOBRAMENTO] Houve DIFAL?
   ├─ NÃO → FIM
   └─ SIM → [DESDOBRAMENTO] Tipo de DIFAL?
      ├─ Comercialização → DIFAL, Comercialização
      ├─ Consumo/Imobilizado → DIFAL, Consumo/Imobilizado
      └─ Ambos → DIFAL - Comercialização e Consumo/Imobilizado
```

### **Fluxo Alternativo - Com Movimento:**

```
Simples Nacional Com Movimento
│
├─ [DESDOBRAMENTO] KEA ultrapassou 3.6?
│  ├─ NÃO → Continua
│  └─ SIM → Recolhimento ISS por fora da DAS
│
├─ Validar importações & Conferência
├─ Apuração e Transmissão PGDAS
├─ DAS - Validação de Entregas
│
└─ [DESDOBRAMENTO] Houve DIFAL?
   └─ (mesmo fluxo anterior)
```

### **Fluxo REINF:**

```
Gerar Obrigações - REINF
│
└─ [DESDOBRAMENTO] Houve Fato Gerador EFD REINF?
   ├─ NÃO → Dispensa de Entrega - EFD REINF
   └─ SIM → Gerar Obrigações REINF
```

---

## 📊 Dados Extraíveis da API

### **Nível 1 - Cabeçalho do Processo**
| Campo | Tipo | Exemplo | Descrição |
|-------|------|---------|-----------|
| ProcID | String | "12345" | ID único do processo |
| ProcNome | String | "Simples Nacional - Mensal" | Nome da matriz |
| ProcTitulo | String | "Simples Nacional - Mensal" | Título do processo |
| ProcCriador | String | "João Silva" | Quem criou |
| ProcGestor | String | "Maria Santos" | Gestor responsável |
| ProcObservacoes | Text | "" | Observações gerais |
| ProcInicio | Date | "11/07/2024" | Data de início |
| ProcDiasCorridos | Integer | "30" | Dias desde início |
| ProcConclusao | Date | "20/08/2024" | Conclusão ou previsão |
| ProcDepartamento | String | "Fiscal" | Departamento principal |
| ProcStatus | String | "Em andamento" | Status atual |
| ProcPorcentagem | String | "45%" | % de conclusão |
| DtLastDH | DateTime | "17/11/2024 10:30:15" | Última alteração |
| EmpNome | String | "Empresa XPTO LTDA" | Nome da empresa |
| EmpID | Integer | "100" | ID da empresa |
| EmpCNPJ | String | "11.111.111/0001-01" | CNPJ |

### **Nível 2 - Passos do Processo (ProcPassos)**
Para cada passo:
| Campo | Tipo | Valores Possíveis |
|-------|------|-------------------|
| Tipo | String | "Passo simples", "Sub processo", "Follow up", "Desdobramento" |
| Status | String | "OK", "Pendente", "Em andamento" |
| Nome | String | Descrição do passo |
| Automacao.Entrega.Tipo | String | "Tarefa", "Obrigação" |
| Automacao.Entrega.Nome | String | Nome da tarefa/obrigação |
| Automacao.Entrega.Criacao | String | Momento de criação |
| Automacao.Entrega.Previsao | String | Tempo estimado |
| Automacao.Entrega.Responsavel | String | Nome do responsável |
| Automacao.Entrega.Prazo | Date | Data limite |
| Automacao.Bloqueante | String | "Sim", "Não" |
| Automacao.Quando | String | Trigger do follow-up |
| Automacao.Para | String | E-mail destinatário |

### **Nível 3 - Desdobramentos (Decisões)**
| Campo | Descrição |
|-------|-----------|
| Nome da decisão | Ex: "Houve DIFAL na competência?" |
| Alternativa escolhida | Ex: "Sim", "Não", "Comercialização" |
| Ação resultante | Qual sub-processo ou passo foi acionado |
| Todas opções disponíveis | Array de todas alternativas possíveis |

---

## 🎯 Análises Possíveis

### **1. Análise de Fluxo e Decisões**
- ✅ Mapear qual caminho cada empresa seguiu
- ✅ Identificar padrão de decisões por empresa
- ✅ Empresas que sempre têm DIFAL
- ✅ Empresas que sempre recolhem ICMS/ISS fora da DAS
- ✅ % empresas sem faturamento vs com movimento
- ✅ Distribuição de tipos de DIFAL
- ✅ Empresas que ultrapassam KEA 3.6

### **2. Análise de Performance**
- ✅ Tempo médio de conclusão por matriz de processo
- ✅ Tempo em cada passo (identificar gargalos)
- ✅ Comparação de tempo entre empresas similares
- ✅ Taxa de conclusão no prazo
- ✅ Processos atrasados e seus passos bloqueados
- ✅ Velocidade de resposta a follow-ups

### **3. Análise de Responsabilidade**
- ✅ Distribuição de trabalho por gestor
- ✅ Carga de trabalho por departamento
- ✅ Responsáveis por cada tipo de passo
- ✅ Follow-ups mais disparados

### **4. Análise de Padrões e Exceções**
- ✅ Empresas com comportamento recorrente idêntico
- ✅ Anomalias (empresas que mudam de padrão)
- ✅ Sazonalidade de decisões
- ✅ Correlação entre regime tributário e decisões

### **5. Análise de Automações**
- ✅ Passos bloqueantes mais frequentes
- ✅ Tarefas vs Obrigações geradas
- ✅ Previsão vs realização de prazos
- ✅ Efetividade de follow-ups

---

## 📋 Estrutura de Dados para Planilha Bruta

### **Aba 1: Processos - Visão Geral**
```
PROC_ID | EMPRESA | CNPJ | MATRIZ_PROCESSO | STATUS | INICIO | CONCLUSAO | DIAS | % | GESTOR | DPTO | ULTIMA_ALT
```

### **Aba 2: Processos - Passos Detalhados**
```
PROC_ID | EMPRESA | PASSO_ORDEM | PASSO_TIPO | PASSO_NOME | PASSO_STATUS | BLOQUEANTE | RESPONSAVEL | PRAZO
```

### **Aba 3: Processos - Desdobramentos**
```
PROC_ID | EMPRESA | DESDOBRAMENTO_NOME | ALTERNATIVA_ESCOLHIDA | ACAO_RESULTANTE | DATA_DECISAO
```

### **Aba 4: Processos - Follow-ups**
```
PROC_ID | EMPRESA | FOLLOWUP_NOME | DESTINATARIO | QUANDO | STATUS
```

### **Aba 5: Análise - Decisões por Empresa**
```
EMPRESA | CNPJ | TEM_DIFAL | TIPO_DIFAL | ICMS_FORA_DAS | ISS_FORA_DAS | KEA_ACIMA_36 | SEM_FATURAMENTO
```

### **Aba 6: Análise - Performance**
```
EMPRESA | CNPJ | TOTAL_PROCESSOS | MEDIA_DIAS | DENTRO_PRAZO | ATRASADOS | PASSO_MAIS_DEMORADO
```

---

## 🔍 Pontos de Atenção Identificados

### **Desdobramentos Críticos:**
1. **Houve DIFAL?** - Decisão que ramifica o processo significativamente
2. **Tipo de DIFAL** - Gera 3 caminhos diferentes
3. **KEA ultrapassou 3.6?** - Impacta recolhimento de ISS

### **Passos Bloqueantes:**
- Validar importações & Conferência de Documentos
- Apuração e Transmissão do PGDAS
- DAS - Validação de Entregas

### **Follow-ups Recorrentes:**
- Sempre há 3 follow-ups por matriz
- E-mails específicos para cada tipo de notificação
- Alguns são disparos manuais, outros automáticos

---

**Última atualização:** 17 de Novembro de 2025  
**Base:** Análise de 12 matrizes de processos do Simples Nacional  
**Status:** Estrutura completa mapeada ✅
