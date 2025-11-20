# 📊 DASHBOARD DE GESTÃO - Simples Nacional

## 🎯 Objetivo: Gestão Visual e Prática

Criar um sistema de gestão que permita **BATER O OLHO e SABER** o status completo dos processos.

---

## 📋 ESTRUTURA EXPANDIDA DA PLANILHA

### **🎯 ABA 1: DASHBOARD** (Visão Executiva)
**Objetivo:** Métricas principais em destaque, números consolidados

| Seção | Métrica | Cálculo | Visualização |
|-------|---------|---------|--------------|
| **📊 GERAL** | | | |
| | Total de Empresas | COUNT DISTINCT(Empresa) | **Número grande** |
| | Processos Ativos | COUNT onde Status=Andamento | **Número grande** |
| | Processos Concluídos | COUNT onde Status=Concluído | **Número grande** |
| | Taxa de Conclusão | (Concluídos / Total) × 100 | **% em destaque** |
| **⏱️ TEMPO** | | | |
| | Tempo Médio Conclusão | AVG(Dias) dos concluídos | **X dias** |
| | Mais Rápido | MIN(Dias) | **X dias** |
| | Mais Lento | MAX(Dias) | **X dias** |
| | Desvio Padrão | STDEV(Dias) | **± X dias** |
| **🚨 ALERTAS** | | | |
| | Processos Atrasados | COUNT onde Dias > Previsão | **🔴 Número** |
| | Vencendo Hoje | COUNT onde Conclusão = HOJE | **🟡 Número** |
| | Vencendo em 3 dias | COUNT onde Conclusão ≤ HOJE+3 | **🟡 Número** |
| | Travados (>15 dias no mesmo passo) | COUNT análise de passos | **🔴 Número** |
| **📈 PERFORMANCE** | | | |
| | Dentro do Prazo | COUNT onde concluiu antes | **🟢 Número** |
| | Fora do Prazo | COUNT onde atrasou | **🔴 Número** |
| | Taxa no Prazo | % dentro prazo | **% verde/vermelho** |
| **👥 GESTORES** | | | |
| | Top Gestor (mais processos) | MODE(Gestor) | **Nome + qtd** |
| | Gestor com melhor média | MIN(AVG dias por gestor) | **Nome + dias** |
| | Distribuição | COUNT por gestor | **Tabela pequena** |

**Layout Visual:**
```
┌─────────────────────────────────────────────────────────┐
│  📊 DASHBOARD - SIMPLES NACIONAL - NOVEMBRO/2024        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  TOTAL EMPRESAS          PROCESSOS ATIVOS               │
│       250                      45                       │
│                                                         │
│  CONCLUÍDOS              TAXA CONCLUSÃO                 │
│       205                     82%  [████████░░]         │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  ⏱️ TEMPO MÉDIO: 12 dias  |  🟢 DENTRO PRAZO: 187      │
│  🏃 MAIS RÁPIDO: 5 dias   |  🔴 ATRASADOS: 18          │
│  🐌 MAIS LENTO: 45 dias   |  🟡 VENCENDO HOJE: 3       │
├─────────────────────────────────────────────────────────┤
│  🚨 ALERTAS CRÍTICOS                                    │
│  • 5 processos travados há mais de 15 dias              │
│  • 8 processos vencendo nos próximos 3 dias             │
│  • 3 empresas com múltiplos processos atrasados         │
└─────────────────────────────────────────────────────────┘
```

---

### **📋 ABA 2: ACOMPANHAMENTO** (Lista Operacional)
**Objetivo:** Lista completa com status visual para acompanhamento diário

| Coluna | Dados | Formato | Propósito |
|--------|-------|---------|-----------|
| 🚦 STATUS | Semáforo visual | 🟢🟡🔴 | Identificação rápida |
| EMPRESA | Nome | Texto | Identificação |
| CNPJ | CNPJ | Formatado | Referência |
| PROCESSO_ID | ID | Número | Rastreio |
| MATRIZ | Nome da matriz | Texto | Tipo de processo |
| DIAS_CORRIDOS | Dias desde início | Número | Tempo decorrido |
| PREVISÃO_CONCLUSÃO | Data prevista | Data | Meta |
| DIAS_RESTANTES | Dias até conclusão | Número + cor | Urgência |
| % CONCLUÍDO | Porcentagem | % + barra | Progresso |
| PASSO_ATUAL | Descrição | Texto | Onde está |
| RESPONSÁVEL | Nome | Texto | Quem cuida |
| ÚLTIMA_ATUALIZAÇÃO | Data/hora | DateTime | Última movimentação |
| AÇÃO_NECESSÁRIA | Próximo passo | Texto | O que fazer |

**Regras de Semáforo:**
- 🟢 **VERDE:** No prazo, andando normalmente (Dias < 80% da previsão)
- 🟡 **AMARELO:** Atenção (Dias entre 80-100% da previsão)
- 🔴 **VERMELHO:** Atrasado (Dias > 100% da previsão) OU Travado
- ⚫ **CINZA:** Concluído

**Ordenação padrão:** Mais críticos primeiro (Vermelho → Amarelo → Verde)

---

### **🚨 ABA 3: ALERTAS** (Processos Críticos)
**Objetivo:** Foco total no que precisa de atenção AGORA

#### **Seção 1: ATRASADOS 🔴**
| Coluna | Dados |
|--------|-------|
| EMPRESA | Nome |
| PROCESSO | Matriz |
| DIAS_ATRASO | Quantos dias passou do prazo |
| PASSO_TRAVADO | Onde está parado |
| RESPONSÁVEL | Quem deve agir |
| ÚLTIMO_MOVIMENTO | Quando mexeu pela última vez |
| AÇÃO_URGENTE | O que fazer |

#### **Seção 2: VENCENDO HOJE/PRÓXIMOS 3 DIAS 🟡**
| Coluna | Dados |
|--------|-------|
| EMPRESA | Nome |
| PROCESSO | Matriz |
| VENCIMENTO | Data |
| HORAS_RESTANTES | Tempo até vencer |
| % CONCLUÍDO | Quanto já foi feito |
| RESPONSÁVEL | Quem está |
| PRIORIDADE | Alta/Média baseada em % |

#### **Seção 3: TRAVADOS (sem movimento >15 dias) ⚫**
| Coluna | Dados |
|--------|-------|
| EMPRESA | Nome |
| PROCESSO | Matriz |
| DIAS_SEM_MOVIMENTO | Quanto tempo parado |
| PASSO_TRAVADO | Onde parou |
| MOTIVO_POSSÍVEL | Análise (bloqueante? falta doc?) |
| RESPONSÁVEL | Quem deve resolver |

---

### **🏆 ABA 4: RANKING** (Performance por Empresa)
**Objetivo:** Identificar padrões, melhores/piores desempenhos

| Coluna | Dados | Uso |
|--------|-------|-----|
| POSIÇÃO | 1, 2, 3... | Ranking |
| EMPRESA | Nome | Identificação |
| CNPJ | CNPJ | Referência |
| TOTAL_PROCESSOS | Quantidade | Volume |
| CONCLUÍDOS | Quantidade | Conclusões |
| EM_ANDAMENTO | Quantidade | Pendentes |
| MÉDIA_DIAS | Tempo médio | Velocidade |
| MELHOR_TEMPO | Processo mais rápido | Mínimo |
| PIOR_TEMPO | Processo mais lento | Máximo |
| CONSISTÊNCIA | Desvio padrão | Previsibilidade |
| TAXA_SUCESSO | % no prazo | Qualidade |
| CLASSIFICAÇÃO | ⭐⭐⭐⭐⭐ | Nota visual |
| TENDÊNCIA | ↗️ ↘️ → | Melhorando/Piorando |

**Classificação (Estrelas):**
- ⭐⭐⭐⭐⭐ = Média < 10 dias + Taxa sucesso > 90%
- ⭐⭐⭐⭐ = Média < 15 dias + Taxa sucesso > 80%
- ⭐⭐⭐ = Média < 20 dias + Taxa sucesso > 70%
- ⭐⭐ = Média < 25 dias OU Taxa sucesso > 60%
- ⭐ = Demais casos

**Ordenação:** Por classificação (5★ → 1★), depois por média de dias

---

### **📊 ABA 5: ANÁLISE_DECISÕES** (Padrões de Decisão)
**Objetivo:** Entender comportamento das empresas

| Coluna | Dados | Análise |
|--------|-------|---------|
| EMPRESA | Nome | - |
| CNPJ | CNPJ | - |
| TOTAL_PROCESSOS | Qtd | Volume |
| % TEM_DIFAL | Percentual | Padrão tributário |
| TIPO_DIFAL_COMUM | Mais frequente | Característica |
| % ICMS_FORA_DAS | Percentual | Padrão recolhimento |
| % ISS_FORA_DAS | Percentual | Padrão recolhimento |
| % SEM_FATURAMENTO | Percentual | Sazonalidade |
| % KEA_ACIMA_36 | Percentual | Padrão faturamento |
| PERFIL | Classificação | "Estável", "Variável", "Complexo" |
| COMPLEXIDADE | 1-5 | Quanto mais desdobramentos |

**Perfis:**
- **Estável:** Sempre segue mesmo caminho (>80% iguais)
- **Variável:** Alterna conforme mês
- **Complexo:** Muitos desdobramentos sempre

---

### **📈 ABA 6: HISTÓRICO_TEMPORAL** (Evolução no Tempo)
**Objetivo:** Identificar tendências e sazonalidade

| Coluna | Dados |
|--------|-------|
| COMPETÊNCIA | Mês/Ano (MM/YYYY) |
| TOTAL_PROCESSOS | Quantidade |
| MÉDIA_DIAS | Tempo médio |
| % NO_PRAZO | Taxa sucesso |
| MAIS_RÁPIDO | Menor tempo |
| MAIS_LENTO | Maior tempo |
| GESTOR_PRINCIPAL | Quem mais atuou |
| DESDOBRAMENTOS_COMUNS | Padrões do mês |

**Permite identificar:**
- Meses mais problemáticos
- Evolução de performance
- Sazonalidade (dezembro sempre pior?)
- Impacto de mudanças de gestor

---

### **🎯 ABA 7: METAS_E_KPIS** (Indicadores de Gestão)
**Objetivo:** Acompanhar evolução vs metas estabelecidas

| KPI | Meta | Atual | Status | Evolução |
|-----|------|-------|--------|----------|
| Tempo Médio Conclusão | ≤ 12 dias | X dias | 🟢/🔴 | ↗️↘️ |
| Taxa de Conclusão no Prazo | ≥ 90% | X% | 🟢/🔴 | ↗️↘️ |
| Processos Atrasados | ≤ 5 | X | 🟢/🔴 | ↗️↘️ |
| Processos Travados | 0 | X | 🟢/🔴 | ↗️↘️ |
| Taxa de Utilização Gestores | 80-100% | X% | 🟢/🔴 | ↗️↘️ |
| Variação de Tempo | ≤ 3 dias | X dias | 🟢/🔴 | ↗️↘️ |

---

### **📊 ABA 8: GARGALOS** (Análise de Passos)
**Objetivo:** Identificar quais passos mais atrasam

| Coluna | Dados |
|--------|-------|
| PASSO_NOME | Descrição |
| TIPO | Simples/Desdobramento/Follow-up |
| OCORRÊNCIAS | Quantas vezes aparece |
| TEMPO_MÉDIO | Média de dias neste passo |
| TEMPO_MAX | Maior tempo registrado |
| % TRAVAMENTOS | Quantos ficam travados aqui |
| RESPONSÁVEL_COMUM | Quem mais cuida |
| BLOQUEANTE | Sim/Não |
| AÇÃO_SUGERIDA | Como melhorar |

**Ordenação:** Por tempo médio (maiores gargalos primeiro)

---

## 🎨 FORMATAÇÃO CONDICIONAL E VISUAL

### **Cores e Semáforos:**

#### **Status Geral:**
- 🟢 **Verde:** Tudo OK, no prazo
- 🟡 **Amarelo:** Atenção necessária
- 🔴 **Vermelho:** Crítico, atrasado
- ⚫ **Cinza:** Concluído
- 🔵 **Azul:** Informativo

#### **Barras de Progresso:**
```
% CONCLUSÃO:
0-30%:   [███░░░░░░░] 🔴
31-60%:  [██████░░░░] 🟡
61-90%:  [████████░░] 🟡
91-100%: [██████████] 🟢
```

#### **Dias Restantes:**
```
< 0 dias:      🔴 ATRASADO
0-3 dias:      🔴 URGENTE
4-7 dias:      🟡 ATENÇÃO
8-15 dias:     🟡 MONITORAR
> 15 dias:     🟢 NO PRAZO
```

### **Destacar Linhas:**
- Linhas de processos atrasados: **Fundo vermelho claro**
- Linhas vencendo hoje: **Fundo amarelo claro**
- Top 3 performers: **Fundo verde claro** (na aba Ranking)
- Bottom 3 performers: **Fundo vermelho claro** (na aba Ranking)

---

## 📱 RESUMO EXECUTIVO (Primeira Página)

### **Layout Sugerido:**

```
┌─────────────────────────────────────────────────────────────────┐
│  GESTÃO SIMPLES NACIONAL - COMPETÊNCIA: NOVEMBRO/2024           │
│  Atualizado em: 17/11/2024 15:30                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📊 VISÃO GERAL                                                 │
│  ───────────────────────────────────────────────────────────── │
│                                                                 │
│   Total Empresas: 250        Processos Ativos: 45              │
│   Concluídos: 205            Taxa: 82% [████████░░]            │
│                                                                 │
│  ⏱️ PERFORMANCE                                                 │
│  ───────────────────────────────────────────────────────────── │
│                                                                 │
│   Tempo Médio: 12 dias       Dentro do Prazo: 187 (91%)        │
│   Mais Rápido: 5 dias        Fora do Prazo: 18 (9%)            │
│   Mais Lento: 45 dias        Meta: ≤12 dias [✓ ATINGIDA]       │
│                                                                 │
│  🚨 ALERTAS (REQUER AÇÃO)                                       │
│  ───────────────────────────────────────────────────────────── │
│                                                                 │
│   🔴 Atrasados: 8 processos                                    │
│   🟡 Vencendo Hoje: 3 processos                                │
│   🟡 Vencendo 3 dias: 5 processos                              │
│   ⚫ Travados >15 dias: 2 processos                             │
│                                                                 │
│  👥 DISTRIBUIÇÃO GESTORES                                       │
│  ───────────────────────────────────────────────────────────── │
│                                                                 │
│   Maria Silva: 25 processos (média 11 dias) ⭐⭐⭐⭐⭐          │
│   João Santos: 20 processos (média 13 dias) ⭐⭐⭐⭐            │
│                                                                 │
│  🏆 TOP 5 EMPRESAS MAIS RÁPIDAS                                 │
│  ───────────────────────────────────────────────────────────── │
│                                                                 │
│   1. Empresa ABC LTDA        - 6 dias  ⭐⭐⭐⭐⭐               │
│   2. Empresa XYZ S.A.        - 7 dias  ⭐⭐⭐⭐⭐               │
│   3. Comércio 123            - 8 dias  ⭐⭐⭐⭐                 │
│                                                                 │
│  ⚠️ EMPRESAS CRÍTICAS (PRECISAM ATENÇÃO)                        │
│  ───────────────────────────────────────────────────────────── │
│                                                                 │
│   • Empresa AAA - 45 dias, travada no passo "Validação"        │
│   • Empresa BBB - 38 dias, 3 processos atrasados               │
│   • Empresa CCC - 32 dias, sem movimento há 15 dias            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 ATUALIZAÇÃO E SINCRONIZAÇÃO

### **Frequência Sugerida:**
- **Tempo real (ideal):** A cada chamada da API
- **Prático:** 2-3x por dia (manhã, tarde, noite)
- **Mínimo:** 1x por dia (início do expediente)

### **Versionamento:**
- Salvar histórico diário: `SimplesNacional_YYYYMMDD_HHMMSS.xlsx`
- Manter "última versão" sempre atualizada: `SimplesNacional_ATUAL.xlsx`

---

## 📊 RELATÓRIOS ADICIONAIS SUGERIDOS

### **1. Relatório Semanal (Sexta-feira)**
- Resumo da semana
- Processos concluídos vs iniciados
- Alertas para próxima semana
- Top/Bottom performers

### **2. Relatório Mensal (Fim do mês)**
- Consolidação total do mês
- Comparativo com mês anterior
- Evolução de KPIs
- Recomendações

### **3. Relatório por Gestor**
- Performance individual
- Processos sob responsabilidade
- Taxa de sucesso
- Pontos de melhoria

---

## 🎯 PRÓXIMA IMPLEMENTAÇÃO

Com essa estrutura, você terá:

✅ **Visão Imediata:** Dashboard com números principais  
✅ **Lista Operacional:** Acompanhamento empresa por empresa  
✅ **Alertas Críticos:** Foco no que precisa ação AGORA  
✅ **Rankings:** Identificar padrões bons/ruins  
✅ **Análise de Decisões:** Entender comportamento  
✅ **Histórico:** Ver evolução no tempo  
✅ **KPIs:** Medir contra metas  
✅ **Gargalos:** Identificar onde melhorar processos  

**Total:** 8 abas de gestão + 3 abas de dados brutos = **11 abas** na planilha

---

**Pronto para implementar?** 🚀
