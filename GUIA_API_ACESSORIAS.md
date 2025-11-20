# Guia Completo da API Acessórias - Documentação para IA

## Índice
1. [Visão Geral](#visão-geral)
2. [Autenticação](#autenticação)
3. [Rate Limiting](#rate-limiting)
4. [Endpoints Disponíveis](#endpoints-disponíveis)
5. [Códigos de Erro](#códigos-de-erro)
6. [Boas Práticas](#boas-práticas)

---

## Visão Geral

**Base URL**: `https://api.acessorias.com`

A API Acessórias é uma interface RESTful que permite integração com o sistema de gestão contábil Acessórias. Ela oferece funcionalidades para:
- Gerenciar empresas (consulta, criação, atualização)
- Gerenciar contatos de empresas
- Consultar entregas e obrigações
- Consultar boletos e faturas
- Consultar e gerenciar processos
- Enviar arquivos para processamento automatizado (e-Contínuo)

---

## Autenticação

### Tipo de Autenticação
**Bearer Authentication** via Header HTTP

### Como Obter o Token
1. Acesse o Sistema Acessórias
2. Clique no botão de "engrenagem" (⚙️) no canto superior direito
3. Selecione "API Token"
4. Copie o token gerado

### Como Usar
Inclua o token em todas as requisições no header:
```
Authorization: Bearer {seu_token_secreto}
```

### Exemplo de Header
```http
Authorization: Bearer secret_key
```

---

## Rate Limiting

### Limite de Requisições
- **100 requisições por minuto**
- Algoritmo: **Sliding Window**
- Funcionamento: Novos slots são liberados conforme slots antigos expiram

### Resposta ao Exceder o Limite
- **HTTP Status Code**: `429 Too Many Requests`

### Recomendações
- Implemente retry com backoff exponencial
- Monitore o número de requisições
- Distribua chamadas ao longo do tempo quando possível

---

## Endpoints Disponíveis

### 1. Companies (Empresas)

#### 1.1 Consultar Empresas

**Endpoint**: `GET /companies/{identificador}`

**Parâmetros de URL**:
- `{identificador}` (obrigatório): CNPJ, CPF ou `ListAll` para listar todas

**Query Parameters**:
- `obligations` (opcional): Incluir para retornar as obrigações da empresa
- `Pagina` (opcional): Número da página (padrão: 1, limite: 20 registros/página)

**Exemplo de Requisição**:
```bash
GET /companies/432.612.527-66/?obligations&Pagina=1
```

**Exemplo de Resposta**:
```json
{
    "ID": "1",
    "Identificador": "432.612.527-66",
    "Razao": "Razão Social da Empresa LTDA",
    "Fantasia": "Fantasia da Empresa",
    "Obrigacoes": [
        {
            "Nome": "INSS / GPS",
            "Status": "Ativa",
            "Entregues": "0",
            "Atrasadas": "4",
            "Proximos30D": "1",
            "Futuras30+": "3"
        }
    ]
}
```

**Campos de Resposta**:
- `ID`: Identificador interno da empresa
- `Identificador`: CNPJ/CPF
- `Razao`: Razão social
- `Fantasia`: Nome fantasia
- `Obrigacoes`: Array de obrigações (quando solicitado)
  - `Nome`: Nome da obrigação
  - `Status`: "Ativa" ou "Inativa nessa empresa"
  - `Entregues`: Quantidade de entregas realizadas
  - `Atrasadas`: Quantidade de entregas atrasadas
  - `Proximos30D`: Entregas nos próximos 30 dias
  - `Futuras30+`: Entregas futuras após 30 dias

---

#### 1.2 Incluir/Editar Empresas

**Endpoint**: `POST /companies`

**Campos do Body**:

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `cnpj` | String | ✅ | CNPJ, CPF ou CAEPF (se já existe, atualiza) |
| `nome` | String | ✅ | Razão social |
| `fantasia` | String | ✅ | Nome fantasia |
| `id` | Integer | ❌ | ID da empresa |
| `getid` | Char (S/N) | ❌ | Se 'S', busca próximo ID disponível (padrão: 'N') |
| `dtcadastro` | Date (Y-m-d) | ❌ | Data de cadastro |
| `dtclidesde` | Date (Y-m-d) | ❌ | Data entrada no escritório |
| `dtcliate` | Date (Y-m-d) | ❌ | Data saída do escritório |
| `regime` | Integer | ❌ | ID do regime tributário (ver tabela abaixo) |
| `dtabertura` | Date (Y-m-d) | ❌ | Data de abertura |
| `inscmunicipal` | String | ❌ | Inscrição municipal |
| `dtinscmunicipal` | Date (Y-m-d) | ❌ | Data inscrição municipal |
| `nire` | String | ❌ | NIRE |
| `apelido` | String | ❌ | Apelido para e-Contínuo |
| `endlogradouro` | String | ❌ | Endereço |
| `endnumero` | String | ❌ | Número |
| `endcomplemento` | String | ❌ | Complemento |
| `cep` | String | ❌ | CEP |
| `bairro` | String | ❌ | Bairro |
| `cidade` | String | ❌ | Cidade |
| `uf` | String | ❌ | Estado (sigla) |
| `codibge` | String | ❌ | Código IBGE |
| `website` | String | ❌ | Website |
| `fone` | String | ❌ | Telefone |
| `honorario` | Float | ❌ | Valor honorário (ex: 1580.98) |
| `ativa` | String (S/N) | ❌ | Empresa ativa? (padrão: 'S') |

**Regimes Tributários**:
| ID | Descrição |
|----|-----------|
| 0 | Indefinido |
| 1 | Simples nacional com inscrição estadual |
| 2 | Simples nacional sem inscrição estadual |
| 3 | Lucro presumido com inscrição estadual - indústria/comércio |
| 4 | Lucro presumido sem inscrição estadual - serviço |
| 5 | Lucro Real |
| 6 | MEI - Micro Empreendedor Individual |
| 7 | Domésticas/Caseiro - e-Social |
| 8 | Produtor Rural |
| 9 | Pessoa Física |
| 10 | Imune/Isenta |

**Exemplo de Resposta (Inclusão)**:
```json
{
    "id": "1",
    "msg": "Empresa 1 criada com sucesso!"
}
```

**Exemplo de Resposta (Atualização)**:
```json
{
    "id": "1",
    "msg": "Empresa 1 atualizada com sucesso!"
}
```

---

### 2. Contacts (Contatos)

#### 2.1 Incluir/Editar Contatos

**Endpoint**: `POST /contacts/{identificador}`

**Parâmetros de URL**:
- `{identificador}` (obrigatório): CNPJ/CPF da empresa

**Campos do Body**:

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `nome` | String | ✅ | Nome do contato |
| `email` | String | ✅ | E-mail válido |
| `cargo` | String | ❌ | Cargo do contato |
| `fone` | String | ❌ | Telefone/Celular |
| `dptos` | Char (S/N) | ❌ | Marcar todos departamentos (padrão: 'S') |

**Exemplo de Resposta (Inclusão)**:
```json
{
    "msg": "Contato criado com sucesso!"
}
```

**Exemplo de Resposta (Atualização)**:
```json
{
    "msg": "Contato atualizado com sucesso!"
}
```

---

### 3. Deliveries (Entregas)

#### 3.1 Consultar Entregas

**Endpoint**: `GET /deliveries/{identificador}`

**Parâmetros de URL**:
- `{identificador}` (obrigatório): CNPJ, CPF ou `ListAll`

**Query Parameters**:

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `DtInitial` | Date (YYYY-MM-DD) | ✅ | Data inicial do prazo |
| `DtFinal` | Date (YYYY-MM-DD) | ✅ | Data final do prazo |
| `DtLastDH` | DateTime | ❌ | Lista apenas alteradas após data/hora (YYYY-MM-DD HH:MM:SS) |
| `Pagina` | Integer | ❌ | Número da página (limite: 50 registros/página) |
| `config` | String/Integer | ❌ | Retorna configurações da entrega ou filtra por ID específica |

**Observação Importante sobre DtLastDH**:
- Quando usar `ListAll` no identificador, `DtLastDH` é **obrigatório**
- Neste caso, aceita apenas **dia atual** ou **dia anterior**

**Exemplo de Requisição**:
```bash
GET /deliveries/432.612.527-66/?DtInitial=2021-08-01&DtFinal=2021-08-31&DtLastDH=2024-08-30 07:00:00
```

**Exemplo de Resposta**:
```json
[
    {
        "ID": "1",
        "Identificador": "432.612.527-66",
        "Razao": "Razão Social da Empresa LTDA",
        "Fantasia": "Fantasia da Empresa",
        "Entregas": [
            {
                "Nome": "Guia da Previdência Social",
                "EntDtPrazo": "2021-08-19",
                "EntDtAtraso": "2021-08-20",
                "EntDtEntrega": "2021-08-19",
                "EntMulta": "S",
                "Status": "Entregue",
                "EntGuiaLida": "Guia já acessada/lida",
                "EntLastDH": "2021-08-19 16:02:26",
                "Config": {
                    "EntID": "16350",
                    "Tipo": "O",
                    "ID": "230",
                    "DptoID": "1",
                    "DptoNome": "Financeiro"
                }
            },
            {
                "Nome": "Consulta do e-Social!",
                "EntDtPrazo": "2021-08-19",
                "EntDtAtraso": "2021-08-19",
                "EntDtEntrega": "0000-00-00",
                "EntMulta": "N",
                "Status": "Pendente",
                "EntGuiaLida": "",
                "EntLastDH": "2021-08-19 16:02:26",
                "Config": {
                    "EntID": "16360",
                    "Tipo": "O",
                    "ID": "235",
                    "DptoID": "2",
                    "DptoNome": "Fiscal"
                }
            }
        ]
    }
]
```

**Campos de Resposta**:
- `ID`: ID interno da empresa
- `Identificador`: CNPJ/CPF
- `Razao`: Razão social
- `Fantasia`: Nome fantasia
- `Entregas`: Array de entregas
  - `Nome`: Nome da entrega
  - `EntCompetencia`: Competência (quando aplicável)
  - `EntDtPrazo`: Data do prazo
  - `EntDtAtraso`: Data considerada atraso
  - `EntDtEntrega`: Data da entrega (0000-00-00 = não entregue)
  - `EntMulta`: Possui multa? (S/N)
  - `Status`: "Entregue", "Pendente", "Atrasada!"
  - `EntGuiaLida`: Status de leitura da guia
  - `EntLastDH`: Data/hora última alteração
  - `Config`: Configurações (quando solicitado)
    - `EntID`: ID da entrega
    - `Tipo`: "O" (Obrigação) ou "T" (Tarefa)
    - `ID`: ID da obrigação/tarefa
    - `DptoID`: ID do departamento
    - `DptoNome`: Nome do departamento

---

### 4. Invoices (Boletos)

#### 4.1 Consultar Boletos

**Endpoint**: `GET /invoices/{identificador}`

**Parâmetros de URL**:
- `{identificador}` (obrigatório): CNPJ, CPF ou `Geral`

**Query Parameters** (obrigatório enviar ao menos um par de datas):

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `VIni` | Date (YYYY-MM-DD) | Data inicial vencimento |
| `VFim` | Date (YYYY-MM-DD) | Data final vencimento |
| `VOIni` | Date (YYYY-MM-DD) | Data inicial vencimento original |
| `VOFim` | Date (YYYY-MM-DD) | Data final vencimento original |
| `PgtoIni` | Date (YYYY-MM-DD) | Data inicial pagamento |
| `PgtoFim` | Date (YYYY-MM-DD) | Data final pagamento |
| `DtCriaIni` | Date (YYYY-MM-DD) | Data inicial criação |
| `DtCriaFim` | Date (YYYY-MM-DD) | Data final criação |
| `DtLast` | Date (YYYY-MM-DD) | Lista apenas alterados após esta data |
| `bltFat` | Char (S/N) | Se 'S', retorna detalhes da fatura (padrão: 'N') |
| `bStatus` | Char | Filtro status: P=Pendentes, Q=Quitados, C=Cancelados |
| `bID` | Integer | ID específico do boleto |
| `Pagina` | Integer | Número da página (limite: 20 registros/página) |

**Exemplo de Requisição**:
```bash
GET /invoices/11.111.111/0001-01/?VOIni=2025-11-01&VOFim=2025-11-31&bStatus=Q&bltFat=S
```

**Exemplo de Resposta**:
```json
[
    {
        "IDBoleto": "56212",
        "Empresa": "Empresa XPTO",
        "EmpID": 1,
        "CNPJ": "11.111.111/0001-01",
        "Competencia": "04/2023",
        "VctoOriginal": "01/05/2023",
        "Vencimento": "01/05/2023",
        "Pagamento": "02/05/2023",
        "DtCredito": "02/05/2023",
        "Valor": "575,00",
        "VrPago": "575,00",
        "VrTaxa": "2,00",
        "Status": "Q",
        "Nota": "202300000018210",
        "PDFNota": "https://endereco.com",
        "Fatura": [
            {
                "Descricao": "Contabilidade",
                "Valor": "575.00",
                "CodPlContas": "01.01",
                "DescPlContas": "Serviços prestados"
            }
        ]
    }
]
```

**Campos de Resposta**:
- `IDBoleto`: ID do boleto
- `Empresa`: Nome da empresa
- `EmpID`: ID interno da empresa
- `CNPJ`: CNPJ da empresa
- `Competencia`: Competência do boleto
- `VctoOriginal`: Vencimento original
- `Vencimento`: Vencimento atual
- `Pagamento`: Data do pagamento
- `DtCredito`: Data do crédito
- `Valor`: Valor do boleto
- `VrPago`: Valor pago
- `VrTaxa`: Valor da taxa
- `Status`: P (Pendente), Q (Quitado), C (Cancelado)
- `Nota`: Número da nota fiscal
- `PDFNota`: URL do PDF da nota
- `Fatura`: Array de itens da fatura (quando solicitado)
  - `Descricao`: Descrição do item
  - `Valor`: Valor do item
  - `CodPlContas`: Código do plano de contas
  - `DescPlContas`: Descrição do plano de contas

---

### 5. Processes (Processos)

#### 5.1 Consultar Processos

**Endpoint**: `GET /processes/{ProcID}`

**Parâmetros de URL**:
- `{ProcID}` (obrigatório): ID do processo ou `ListAll`

**Query Parameters**:

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `ProcStatus` | Char | A=Andamento, C=Concluídos, S=Suspensos, D=Desistências, P=Agendados, W=Aguardando aprovação, X=Excluídos |
| `ProcNome` | String | Nome ou título do processo |
| `ProcInicioIni` | Date (YYYY-MM-DD) | Data inicial do processo |
| `ProcInicioFim` | Date (YYYY-MM-DD) | Data final do processo |
| `ProcConclusaoIni` | Date (YYYY-MM-DD) | Data inicial conclusão |
| `ProcConclusaoFim` | Date (YYYY-MM-DD) | Data final conclusão |
| `Pagina` | Integer | Número da página (limite: 20 registros/página) |
| `DtLastDH` | DateTime (YYYY-MM-DD HH:MM:SS) | Lista apenas alterados após data/hora |

**Nota**: Processos excluídos (X) não aparecem por padrão, apenas quando buscados especificamente.

**Exemplo de Requisição (Listagem)**:
```bash
GET /processes/ListAll/?ProcStatus=A&Pagina=1
```

**Exemplo de Resposta (Listagem)**:
```json
[
    {
        "ProcID": "12345",
        "ProcNome": "Processo de exemplo",
        "ProcTitulo": "Processo de exemplo",
        "ProcCriador": "Usuário de exemplo",
        "ProcGestor": "Usuário de exemplo",
        "ProcObservacoes": "",
        "ProcInicio": "11/07/2024",
        "ProcDiasCorridos": "1",
        "ProcConclusao": "20/07/2024",
        "ProcDepartamento": "Departamento exemplo",
        "ProcStatus": "Em andamento",
        "ProcPorcentagem": "30%",
        "DtLastDH": "06/12/2024 15:10:12",
        "EmpNome": "Empresa XPTO",
        "EmpID": "1",
        "EmpCNPJ": "11.111.111/0001-01"
    }
]
```

**Exemplo de Requisição (Detalhes)**:
```bash
GET /processes/12345
```

**Exemplo de Resposta (Detalhes com Passos)**:
```json
[
    {
        "ProcID": "12345",
        "ProcNome": "Processo de exemplo",
        "ProcTitulo": "Processo de exemplo",
        "ProcCriador": "Usuário de exemplo",
        "ProcGestor": "Usuário de exemplo",
        "ProcObservacoes": "",
        "ProcInicio": "11/07/2024",
        "ProcDiasCorridos": "1",
        "ProcConclusao": "20/07/2024",
        "ProcDepartamento": "Departamento exemplo",
        "ProcStatus": "Em andamento",
        "ProcPorcentagem": "30%",
        "DtLastDH": "06/12/2024 15:10:12",
        "EmpNome": "Empresa XPTO",
        "EmpID": 1,
        "EmpCNPJ": "11.111.111/0001-01",
        "ProcPassos": [
            {
                "Tipo": "Passo simples",
                "Status": "OK",
                "Nome": "Tarefa pontual",
                "Automacao": {
                    "Entrega": {
                        "Tipo": "Tarefa",
                        "Nome": "Tarefa",
                        "Criacao": "no dia do início/autorização do processo",
                        "Previsao": "30 min",
                        "Responsavel": "Pedro",
                        "Prazo": "18/07/2024"
                    },
                    "Bloqueante": "Sim"
                }
            },
            {
                "Tipo": "Sub processo",
                "Nome": "Definir permissões",
                "ProcPassos": [...]
            },
            {
                "Tipo": "Follow up",
                "Status": "Pendente",
                "Nome": "Avisar ao Dpto de TI",
                "Automacao": {
                    "Quando": "Disparo manual",
                    "Para": "e-mail específico 'Dpto TI'"
                }
            },
            {
                "Tipo": "Desdobramento",
                "Status": "Pendente",
                "Nome": "Qual o Dpto?",
                "Automacao": [
                    {
                        "Nome": "Fiscal",
                        "Acao": {
                            "Tipo": "Sub processo",
                            "Nome": "Novo funcionário - Fiscal"
                        }
                    }
                ]
            }
        ]
    }
]
```

**Tipos de Passos em Processos**:
1. **Passo simples**: Tarefa individual com automação de entrega
2. **Sub processo**: Processo aninhado com seus próprios passos
3. **Follow up**: Notificação/comunicação automática
4. **Desdobramento**: Decisão que leva a diferentes ações

**Campos de Resposta**:
- `ProcID`: ID do processo
- `ProcNome`: Nome do processo
- `ProcTitulo`: Título do processo
- `ProcCriador`: Usuário que criou
- `ProcGestor`: Gestor responsável
- `ProcObservacoes`: Observações
- `ProcInicio`: Data de início
- `ProcDiasCorridos`: Dias decorridos
- `ProcConclusao`: Data de conclusão (ou previsão se não concluído)
- `ProcDepartamento`: Departamento responsável
- `ProcStatus`: Status atual
- `ProcPorcentagem`: Percentual de conclusão
- `DtLastDH`: Data/hora última alteração
- `EmpNome`: Nome da empresa vinculada
- `EmpID`: ID da empresa
- `EmpCNPJ`: CNPJ da empresa
- `ProcPassos`: Array de passos do processo (quando consultado especificamente)

---

### 6. e-Contínuo (Processamento Automatizado)

#### 6.1 Enviar Arquivo para Processamento

**Endpoint**: `POST /econtinuo`

**Content-Type**: `multipart/form-data`

**Campos do Body**:

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `arquivo` | File | ✅ | Arquivo PDF a ser processado |

**Exemplo de Resposta (Sucesso)**:
```json
{
    "msg": "Entrega processada com sucesso! [GPS - Guia da Previdência Social]",
    "pathFolder": "13/Geral/GUIAS/GPS/2022/01/Pessoal/2022-01-GPSMensalpdf.pdf"
}
```

**Exemplo de Resposta (Falha)**:
```json
{
    "Erro": "Entrega [GPS para 30.637.209/0001-21] inexistente [Comp. 01/2022]."
}
```

**Campos de Resposta**:
- `msg`: Mensagem de sucesso
- `pathFolder`: Caminho sugerido para backup local
- `Erro`: Mensagem de erro (quando aplicável)

**Funcionalidade**:
- Robô automatizado que processa PDFs de guias e documentos
- Identifica automaticamente o tipo de documento
- Associa à empresa e competência corretas
- Sugere estrutura de pasta para organização local

---

## Códigos de Erro

A API utiliza códigos HTTP padrão:

| Código | Significado | Descrição |
|--------|-------------|-----------|
| 200 | OK | Requisição bem-sucedida, JSON retornado |
| 204 | No Content | Não existe conteúdo para a requisição |
| 401 | Unauthorized | Token inválido ou incorreto |
| 404 | Not Found | Requisição incorreta ou recurso não encontrado |
| 429 | Too Many Requests | Limite de rate-limit excedido |

---

## Boas Práticas

### 1. Paginação
- Todas as listagens retornam no máximo 20-50 registros por página
- Sempre verifique se há mais páginas incrementando o parâmetro `Pagina`
- Continue até receber uma lista vazia

**Exemplo de Loop de Paginação**:
```python
pagina = 1
todos_registros = []

while True:
    response = get(f"/companies/ListAll/?Pagina={pagina}")
    if not response or len(response) == 0:
        break
    todos_registros.extend(response)
    pagina += 1
```

### 2. Filtros de Data/Hora
- Use `DtLastDH` para sincronizações incrementais
- Evita reprocessar dados já conhecidos
- Reduz consumo de rate-limit

**Exemplo**:
```bash
# Buscar apenas entregas modificadas desde a última sincronização
GET /deliveries/ListAll/?DtInitial=2024-01-01&DtFinal=2024-12-31&DtLastDH=2024-11-17 14:30:00
```

### 3. Gestão de Rate-Limit
- Implemente controle de requisições no cliente
- Use exponential backoff ao receber 429
- Distribua requisições ao longo do tempo

**Exemplo de Estratégia**:
```python
import time

MAX_REQUESTS_PER_MINUTE = 90  # Margem de segurança
requests_count = 0
start_time = time.time()

def fazer_requisicao():
    global requests_count, start_time
    
    # Se passou 1 minuto, reset contador
    if time.time() - start_time > 60:
        requests_count = 0
        start_time = time.time()
    
    # Se atingiu limite, espera
    if requests_count >= MAX_REQUESTS_PER_MINUTE:
        time.sleep(60 - (time.time() - start_time))
        requests_count = 0
        start_time = time.time()
    
    # Faz requisição
    response = api_call()
    requests_count += 1
    return response
```

### 4. Tratamento de Erros
- Sempre valide o status code HTTP
- Trate códigos 401 renovando o token
- Implemente retry para erros temporários (429, timeouts)

### 5. Uso Eficiente de Parâmetros Opcionais
- Use `obligations` apenas quando necessário
- Use `config` em deliveries apenas quando precisar de detalhes
- Use `bltFat=S` apenas quando precisar dos itens da fatura

### 6. Identificadores
- CNPJ/CPF podem ser formatados ou não (11.111.111/0001-01 ou 11111111000101)
- Use `ListAll` para listar todos os registros
- Use `Geral` para boletos de todas as empresas

### 7. Datas
- Sempre use formato ISO (YYYY-MM-DD)
- Para data/hora: YYYY-MM-DD HH:MM:SS
- Campos de data vazios retornam como "0000-00-00"

### 8. Atualização vs Criação
- Endpoints POST geralmente fazem upsert (cria se não existe, atualiza se existe)
- O identificador (CNPJ/CPF/email) é usado para determinar se é update ou insert
- Verifique a mensagem de resposta para confirmar a operação realizada

---

## Casos de Uso Comuns

### Caso 1: Sincronizar Todas as Empresas
```
1. GET /companies/ListAll/?Pagina=1
2. Incrementar Pagina até receber lista vazia
3. Armazenar dados localmente
```

### Caso 2: Monitorar Entregas Atrasadas
```
1. GET /deliveries/ListAll/?DtInitial={data_inicio}&DtFinal={data_fim}
2. Filtrar entregas com Status="Atrasada!"
3. Notificar responsáveis
```

### Caso 3: Atualizar Dados de Empresa
```
1. POST /companies com cnpj existente
2. Enviar apenas campos que deseja atualizar
3. Sistema faz merge com dados existentes
```

### Caso 4: Processar Guias Automaticamente
```
1. Receber PDF de guia
2. POST /econtinuo com arquivo
3. Verificar resposta para confirmar processamento
4. Usar pathFolder para organizar backup
```

### Caso 5: Consultar Status de Processos em Andamento
```
1. GET /processes/ListAll/?ProcStatus=A
2. Analisar ProcPorcentagem e ProcStatus
3. Para detalhes: GET /processes/{ProcID}
4. Verificar ProcPassos para status de cada etapa
```

### Caso 6: Relatório de Boletos Quitados
```
1. GET /invoices/Geral/?VOIni=2025-11-01&VOFim=2025-11-30&bStatus=Q&bltFat=S
2. Processar array Fatura de cada boleto
3. Gerar relatório consolidado
```

---

## Resumo Rápido de Endpoints

| Endpoint | Método | Função Principal |
|----------|--------|------------------|
| `/companies/{id}` | GET | Consultar empresas |
| `/companies` | POST | Criar/atualizar empresa |
| `/contacts/{cnpj}` | POST | Criar/atualizar contato |
| `/deliveries/{id}` | GET | Consultar entregas e obrigações |
| `/invoices/{id}` | GET | Consultar boletos e faturas |
| `/processes/{id}` | GET | Consultar processos e seus passos |
| `/econtinuo` | POST | Enviar PDF para processamento |

---

## Notas Importantes para IA

1. **Sempre valide autenticação** antes de qualquer operação
2. **Respeite o rate-limit** de 100 req/min
3. **Use paginação** corretamente para evitar perda de dados
4. **Formato de datas** é crítico: YYYY-MM-DD
5. **Identificadores** aceitam formatação com ou sem pontuação
6. **Parâmetros opcionais** reduzem payload, use apenas quando necessário
7. **Erro 204** não é erro real, apenas indica ausência de dados
8. **ListAll** sempre requer paginação
9. **DtLastDH** é ideal para sincronizações incrementais
10. **Status codes** seguem padrão HTTP, trate-os adequadamente

---

## Exemplo de Workflow Completo

### Sincronização Diária de Dados

```
1. Obter timestamp da última sincronização
2. GET /companies/ListAll/?DtLast={ultimo_sync} (com paginação)
3. Para cada empresa atualizada:
   a. GET /deliveries/{cnpj}/?DtLastDH={ultimo_sync}
   b. GET /invoices/{cnpj}/?DtLast={ultimo_sync}
4. GET /processes/ListAll/?DtLastDH={ultimo_sync}
5. Atualizar timestamp de sincronização
6. Gerar relatório de mudanças
```

---

**Última atualização**: 17 de Novembro de 2025
**Versão da API**: Atual
**Suporte**: Via sistema Acessórias
