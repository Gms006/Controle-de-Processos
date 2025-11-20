# Estrutura de Dados - Processos

## 📊 Formato de Dados da API

### Processo (Response da API)

```json
{
    "ProcID": "12345",
    "ProcNome": "Simples Nacional - Mensal",
    "ProcTitulo": "Simples Nacional - Mensal",
    "ProcCriador": "Nome do Usuário",
    "ProcGestor": "Nome do Gestor",
    "ProcObservacoes": "Observações do processo",
    "ProcInicio": "11/07/2024",
    "ProcDiasCorridos": "30",
    "ProcConclusao": "20/08/2024",
    "ProcDepartamento": "Fiscal",
    "ProcStatus": "Em andamento",
    "ProcPorcentagem": "45%",
    "DtLastDH": "17/11/2024 10:30:15",
    "EmpNome": "Empresa Exemplo LTDA",
    "EmpID": "100",
    "EmpCNPJ": "11.111.111/0001-01",
    "ProcPassos": []
}
```

## 📋 Estrutura de Planilhas

### Processos Concluídos

| Campo | Tipo | Descrição |
|-------|------|-----------|
| EMPRESA | String | Nome da empresa |
| CNPJ | String | CNPJ formatado |
| PROC_ID | Integer | ID do processo |
| PROCESSO | String | Nome do processo |
| DATA_INICIO | Date | Data de início |
| DATA_CONCLUSAO | Date | Data de conclusão |
| DIAS_CORRIDOS | Integer | Dias totais |
| DEPARTAMENTO | String | Departamento responsável |
| GESTOR | String | Gestor responsável |
| PORCENTAGEM | String | 100% |

### Processos Em Andamento

| Campo | Tipo | Descrição |
|-------|------|-----------|
| EMPRESA | String | Nome da empresa |
| CNPJ | String | CNPJ formatado |
| PROC_ID | Integer | ID do processo |
| PROCESSO | String | Nome do processo |
| DATA_INICIO | Date | Data de início |
| DIAS_CORRIDOS | Integer | Dias decorridos |
| PREV_CONCLUSAO | Date | Previsão de conclusão |
| DEPARTAMENTO | String | Departamento responsável |
| GESTOR | String | Gestor responsável |
| PORCENTAGEM | String | % atual |
| PASSO_ATUAL | String | Nome do passo atual |
| STATUS_PASSO | String | Status do passo |

## 🔄 Status Possíveis

### Status de Processo
- `A` - Em Andamento
- `C` - Concluído
- `S` - Suspenso
- `D` - Desistência
- `P` - Agendado/Pending
- `W` - Aguardando aprovação/Waiting
- `X` - Excluído

### Status de Passo
- `OK` - Concluído
- `Pendente` - Aguardando execução
- `Em andamento` - Sendo executado

## 📁 Armazenamento Local

### Dados Brutos (JSON)
```
data/raw/processos_YYYYMMDD_HHMMSS.json
```

### Dados Processados
```
data/processed/analise_simples_nacional_YYYYMMDD.json
```

### Planilhas Geradas
```
output/planilhas/processos_concluidos_YYYYMMDD.xlsx
output/planilhas/processos_andamento_YYYYMMDD.xlsx
output/planilhas/analise_geral_YYYYMMDD.xlsx
```
