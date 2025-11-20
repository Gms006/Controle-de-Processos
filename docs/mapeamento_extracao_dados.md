# 📊 Mapeamento de Extração de Dados - Simples Nacional

## 🎯 Objetivo
Definir EXATAMENTE quais dados vamos extrair da API `/processes` e como organizar na planilha bruta inicial.

---

## 📡 Endpoint da API

```
GET /processes/ListAll/?ProcStatus=A&ProcNome=Simples Nacional
GET /processes/ListAll/?ProcStatus=C&ProcNome=Simples Nacional
```

**Filtros aplicáveis:**
- `ProcStatus=A` - Em Andamento
- `ProcStatus=C` - Concluídos
- `ProcNome=Simples Nacional` - Filtrar por nome (pode pegar todas variações)
- `DtLastDH=YYYY-MM-DD HH:MM:SS` - Para sincronização incremental

---

## 📋 Estrutura de Dados da API (Resposta Esperada)

### **Response Base:**
```json
[
    {
        "ProcID": "12345",
        "ProcNome": "Simples Nacional - Mensal",
        "ProcTitulo": "Simples Nacional - Mensal",
        "ProcCriador": "Usuário Criador",
        "ProcGestor": "Gestor Responsável",
        "ProcObservacoes": "Observações...",
        "ProcInicio": "11/07/2024",
        "ProcDiasCorridos": "30",
        "ProcConclusao": "20/08/2024",
        "ProcDepartamento": "Fiscal",
        "ProcStatus": "Em andamento",
        "ProcPorcentagem": "45%",
        "DtLastDH": "17/11/2024 10:30:15",
        "EmpNome": "Empresa XPTO LTDA",
        "EmpID": "100",
        "EmpCNPJ": "11.111.111/0001-01",
        "ProcPassos": [...]
    }
]
```

### **ProcPassos (Array de Passos):**
```json
"ProcPassos": [
    {
        "Tipo": "Passo simples",
        "Status": "OK",
        "Nome": "Validar importações & Conferência de Documentos",
        "Automacao": {
            "Entrega": {
                "Tipo": "Tarefa",
                "Nome": "Tarefa exemplo",
                "Criacao": "no dia do início",
                "Previsao": "30 min",
                "Responsavel": "Pedro",
                "Prazo": "18/07/2024"
            },
            "Bloqueante": "Sim"
        }
    },
    {
        "Tipo": "Desdobramento",
        "Status": "OK",
        "Nome": "Houve DIFAL na competência?",
        "Automacao": [
            {
                "Nome": "Sim",
                "Acao": {
                    "Tipo": "Sub processo",
                    "Nome": "Tipo de DIFAL"
                }
            },
            {
                "Nome": "Não",
                "Acao": {
                    "Tipo": "Passo simples",
                    "Nome": "Conclui o passo"
                }
            }
        ]
    },
    {
        "Tipo": "Follow up",
        "Status": "Pendente",
        "Nome": "Avisar departamento",
        "Automacao": {
            "Quando": "Disparo manual",
            "Para": "email@empresa.com"
        }
    },
    {
        "Tipo": "Sub processo",
        "Nome": "Tipo de DIFAL",
        "ProcPassos": [
            {...}
        ]
    }
]
```

---

## 📊 Planilha Bruta - Estrutura Proposta

### **ABA 1: PROCESSOS_GERAL**
Visão consolidada de todos os processos

| Coluna | Origem API | Tipo | Descrição |
|--------|-----------|------|-----------|
| PROC_ID | ProcID | String | ID único |
| EMPRESA | EmpNome | String | Nome da empresa |
| CNPJ | EmpCNPJ | String | CNPJ formatado |
| EMP_ID | EmpID | Integer | ID interno empresa |
| MATRIZ_PROCESSO | ProcNome | String | Nome da matriz do processo |
| TITULO | ProcTitulo | String | Título específico |
| STATUS | ProcStatus | String | Em andamento/Concluído |
| PORCENTAGEM | ProcPorcentagem | String | % conclusão |
| DATA_INICIO | ProcInicio | Date | Data início |
| DATA_CONCLUSAO | ProcConclusao | Date | Conclusão ou previsão |
| DIAS_CORRIDOS | ProcDiasCorridos | Integer | Dias desde início |
| CRIADOR | ProcCriador | String | Quem criou |
| GESTOR | ProcGestor | String | Gestor responsável |
| DEPARTAMENTO | ProcDepartamento | String | Departamento |
| OBSERVACOES | ProcObservacoes | Text | Obs gerais |
| ULTIMA_ALTERACAO | DtLastDH | DateTime | Última modificação |

**Total: 16 colunas**

---

### **ABA 2: PROCESSOS_PASSOS**
Detalhamento de cada passo de cada processo

| Coluna | Origem | Tipo | Descrição |
|--------|--------|------|-----------|
| PROC_ID | ProcID | String | Referência ao processo |
| EMPRESA | EmpNome | String | Nome empresa |
| PASSO_ORDEM | Calculado | Integer | Ordem sequencial (1, 2, 3...) |
| PASSO_TIPO | ProcPassos[].Tipo | String | Passo simples/Follow-up/Desdobramento/Sub processo |
| PASSO_NOME | ProcPassos[].Nome | String | Descrição do passo |
| PASSO_STATUS | ProcPassos[].Status | String | OK/Pendente/Em andamento |
| BLOQUEANTE | ProcPassos[].Automacao.Bloqueante | String | Sim/Não |
| ENTREGA_TIPO | ProcPassos[].Automacao.Entrega.Tipo | String | Tarefa/Obrigação |
| ENTREGA_NOME | ProcPassos[].Automacao.Entrega.Nome | String | Nome da entrega |
| RESPONSAVEL | ProcPassos[].Automacao.Entrega.Responsavel | String | Responsável |
| PRAZO | ProcPassos[].Automacao.Entrega.Prazo | Date | Data limite |
| PREVISAO_TEMPO | ProcPassos[].Automacao.Entrega.Previsao | String | Tempo estimado |
| CRIACAO_QUANDO | ProcPassos[].Automacao.Entrega.Criacao | String | Momento de criação |
| FOLLOWUP_QUANDO | ProcPassos[].Automacao.Quando | String | Quando dispara |
| FOLLOWUP_PARA | ProcPassos[].Automacao.Para | String | Email destino |

**Total: 15 colunas**

---

### **ABA 3: PROCESSOS_DESDOBRAMENTOS**
Mapeia todas as decisões tomadas

| Coluna | Origem | Tipo | Descrição |
|--------|--------|------|-----------|
| PROC_ID | ProcID | String | Referência |
| EMPRESA | EmpNome | String | Nome empresa |
| CNPJ | EmpCNPJ | String | CNPJ |
| DESDOBRAMENTO_ORDEM | Calculado | Integer | Ordem do desdobramento |
| DESDOBRAMENTO_NOME | ProcPassos[Desdobramento].Nome | String | Ex: "Houve DIFAL?" |
| DESDOBRAMENTO_STATUS | ProcPassos[Desdobramento].Status | String | OK/Pendente |
| ALTERNATIVAS_DISPONIVEIS | ProcPassos[].Automacao[].Nome | String | Todas opções (Sim;Não) |
| ALTERNATIVA_ESCOLHIDA | Análise do fluxo | String | Qual foi escolhida |
| ACAO_TIPO | ProcPassos[].Automacao[].Acao.Tipo | String | Sub processo/Passo simples |
| ACAO_NOME | ProcPassos[].Automacao[].Acao.Nome | String | Nome da ação resultante |

**Total: 10 colunas**

---

### **ABA 4: ANALISE_DECISOES**
Análise consolidada de decisões por empresa

| Coluna | Cálculo | Tipo | Descrição |
|--------|---------|------|-----------|
| EMPRESA | EmpNome | String | Nome |
| CNPJ | EmpCNPJ | String | CNPJ |
| TOTAL_PROCESSOS | COUNT | Integer | Total de processos |
| CONCLUIDOS | COUNT onde Status=C | Integer | Concluídos |
| EM_ANDAMENTO | COUNT onde Status=A | Integer | Em andamento |
| TEVE_DIFAL | Análise desdobramento | String | Sim/Não/N/A |
| TIPO_DIFAL | Decisão extraída | String | Comercialização/Consumo/Ambos/N/A |
| ICMS_FORA_DAS | Matriz usada | String | Sim/Não/N/A |
| ISS_FORA_DAS | Matriz usada | String | Sim/Não/N/A |
| KEA_ACIMA_36 | Decisão extraída | String | Sim/Não/N/A |
| SEM_FATURAMENTO | Matriz usada | String | Sim/Não/N/A |
| MATRIZ_PRINCIPAL | ProcNome mais comum | String | Qual matriz mais usa |

**Total: 12 colunas**

---

### **ABA 5: ANALISE_PERFORMANCE**
Métricas de desempenho

| Coluna | Cálculo | Tipo | Descrição |
|--------|---------|------|-----------|
| EMPRESA | EmpNome | String | Nome |
| CNPJ | EmpCNPJ | String | CNPJ |
| TOTAL_PROCESSOS | COUNT | Integer | Total |
| MEDIA_DIAS_CONCLUSAO | AVG(ProcDiasCorridos) | Decimal | Média de dias |
| MIN_DIAS | MIN | Integer | Processo mais rápido |
| MAX_DIAS | MAX | Integer | Processo mais lento |
| DENTRO_PRAZO | COUNT análise | Integer | Concluídos no prazo |
| ATRASADOS | COUNT análise | Integer | Processos atrasados |
| TAXA_CONCLUSAO | % | Decimal | % concluídos/total |
| GESTOR_PRINCIPAL | Mode | String | Gestor mais frequente |
| ULTIMO_PROCESSO | MAX(ProcInicio) | Date | Data último processo |

**Total: 11 colunas**

---

### **ABA 6: ANALISE_PASSOS**
Identificar gargalos em passos específicos

| Coluna | Cálculo | Tipo | Descrição |
|--------|---------|------|-----------|
| PASSO_NOME | Unique | String | Nome do passo |
| TIPO | Tipo | String | Tipo do passo |
| OCORRENCIAS | COUNT | Integer | Quantas vezes aparece |
| SEMPRE_OK | % | Decimal | % marcados como OK |
| MEDIA_RESPONSAVEL | String | String | Responsável mais comum |
| BLOQUEANTE | String | String | Sim/Não |
| OBSERVACOES | Text | Text | Análises adicionais |

**Total: 7 colunas**

---

## 🔄 Lógica de Identificação de Decisões

### **Como identificar qual alternativa foi escolhida:**

1. **Analisar próximos passos:**
   - Se após "Houve DIFAL?" aparece "Tipo de DIFAL" → escolheu SIM
   - Se após "Houve DIFAL?" processo termina → escolheu NÃO

2. **Analisar sub-processos acionados:**
   - Se aparece "DIFAL, Comercialização" → escolheu Comercialização
   - Se aparece "DIFAL, Consumo/Imobilizado" → escolheu Consumo/Imobilizado

3. **Analisar matriz do processo:**
   - Se ProcNome = "Simples Nacional - Sem Faturamento" → empresa SEM faturamento
   - Se ProcNome = "Recolhimento de ISS por fora da DAS" → ISS fora DAS

### **Mapeamento Matriz → Decisão:**

| Matriz do Processo | Implica |
|--------------------|---------|
| Simples Nacional - Sem Faturamento | SEM_FATURAMENTO = Sim |
| Simples Nacional Com Movimento | TEM_MOVIMENTO = Sim |
| Recolhimento de ISS por fora da DAS | ISS_FORA_DAS = Sim |
| Recolhimento de ICMS por fora da DAS | ICMS_FORA_DAS = Sim |
| Recolhimento de ICMS e ISS por fora da DAS | ICMS_FORA_DAS = Sim, ISS_FORA_DAS = Sim |
| Tipo de DIFAL | TEVE_DIFAL = Sim |
| DIFAL, Comercialização | TIPO_DIFAL = Comercialização |
| DIFAL, Consumo/Imobilizado | TIPO_DIFAL = Consumo/Imobilizado |
| DIFAL - Comercialização e Consumo/Imobilizado | TIPO_DIFAL = Ambos |
| Gerar Obrigações - REINF | PRECISA_REINF = Sim |
| Dispensa de Entrega - EFD REINF | PRECISA_REINF = Não |

---

## 🎯 Prioridade de Implementação

### **Fase 1 - Dados Brutos (AGORA):**
✅ Aba 1: PROCESSOS_GERAL  
✅ Aba 2: PROCESSOS_PASSOS  
✅ Aba 3: PROCESSOS_DESDOBRAMENTOS  

### **Fase 2 - Análises (DEPOIS):**
⏳ Aba 4: ANALISE_DECISOES  
⏳ Aba 5: ANALISE_PERFORMANCE  
⏳ Aba 6: ANALISE_PASSOS  

---

## 💾 Formato de Arquivo

**Nome do arquivo:**
```
SimplesNacional_ProcessosBrutos_YYYYMMDD_HHMMSS.xlsx
```

**Exemplo:**
```
SimplesNacional_ProcessosBrutos_20241117_153045.xlsx
```

**Encoding:** UTF-8  
**Formato:** XLSX (Excel)  
**Separador CSV:** ; (ponto e vírgula) - caso exporte CSV

---

## 🔍 Campos Calculados/Derivados

### **PASSO_ORDEM:**
Incrementar sequencialmente para cada passo dentro do mesmo ProcID

### **ALTERNATIVA_ESCOLHIDA:**
Analisar:
1. Status do desdobramento (se OK, decisão foi tomada)
2. Próximos passos/sub-processos que aparecem
3. Nome da matriz do processo

### **DESDOBRAMENTO_ORDEM:**
Incrementar para cada desdobramento no mesmo processo

### **TAXA_CONCLUSAO:**
```
(CONCLUIDOS / TOTAL_PROCESSOS) * 100
```

---

## 📌 Observações Importantes

1. **Processos podem ter sub-processos** → Precisamos iterar recursivamente em ProcPassos
2. **Desdobramentos têm array de opções** → Extrair todas, identificar escolhida
3. **Follow-ups sempre em trio** → Podem ter e-mails hardcoded
4. **Datas em formato BR** → Converter para YYYY-MM-DD para ordenação
5. **Status OK não significa concluído** → OK = passo concluído, não processo
6. **ProcConclusao** → Pode ser data real (concluído) ou previsão (em andamento)

---

## 🚀 Próximos Passos

1. ✅ Documentação completa criada
2. ⏳ Implementar parser de JSON → DataFrame pandas
3. ⏳ Implementar lógica de identificação de decisões
4. ⏳ Implementar exportação para Excel multi-abas
5. ⏳ Testar com dados reais da API
6. ⏳ Refinar análises conforme necessidade

---

**Última atualização:** 17 de Novembro de 2025  
**Status:** Especificação completa para implementação ✅
