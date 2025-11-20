# 📊 Análise de Processos - API Acessórias

Projeto para análise automatizada de processos do sistema Acessórias, com foco inicial em **Simples Nacional - Mensal**.

## 🎯 Objetivo

Buscar, analisar e gerar relatórios sobre processos em andamento e concluídos, identificando:
- Status atual de cada processo
- Onde o processo está parado
- Tempo decorrido e previsão de conclusão
- Análises por empresa
- Gargalos e oportunidades de melhoria

## 📁 Estrutura do Projeto

```
c:\acessorias processos\
├── config/                      # Configurações
│   └── config.json             # Configurações gerais
├── data/                        # Dados
│   ├── raw/                    # Dados brutos da API
│   └── processed/              # Dados processados
├── scripts/                     # Scripts Python
│   ├── api_client.py           # Cliente da API
│   ├── buscar_processos_simples_nacional.py  # Script principal
│   ├── processador_processos.py  # Processamento de dados
│   ├── exportador_excel.py     # Exportação para Excel
│   └── utils.py                # Utilitários
├── docs/                        # Documentação
│   └── estrutura_processo_simples_nacional.md  # Detalhes do processo
├── logs/                        # Logs de execução
├── output/                      # Arquivos de saída
│   ├── planilhas/              # Planilhas Excel geradas
│   └── relatorios/             # Relatórios HTML/PDF
├── .env.example                # Exemplo de variáveis de ambiente
├── .gitignore                  # Arquivos ignorados pelo Git
├── requirements.txt            # Dependências Python
└── README.md                   # Este arquivo
```

## 🚀 Como Usar

### 1. Instalação

```powershell
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
.\venv\Scripts\Activate.ps1

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configuração

```powershell
# Copiar arquivo de exemplo
copy .env.example .env

# Editar .env e adicionar seu token da API
notepad .env
```

### 3. Execução

```powershell
# Buscar processos de Simples Nacional
python scripts\buscar_processos_simples_nacional.py
```

## 📋 Funcionalidades Planejadas

### Fase 1 - Simples Nacional (Atual)
- [x] Estrutura do projeto
- [ ] Buscar processos concluídos
- [ ] Buscar processos em andamento
- [ ] Análise por empresa
- [ ] Identificação de passo atual
- [ ] Exportação para Excel

### Fase 2 - Análises Avançadas
- [ ] Dashboard interativo
- [ ] Alertas de processos atrasados
- [ ] Previsão de conclusão com ML
- [ ] Relatórios automatizados

### Fase 3 - Outros Processos
- [ ] Integração com outros tipos de processo
- [ ] Análise comparativa
- [ ] Benchmarking

## 📊 Saídas Geradas

### Planilhas Excel
1. **Processos Concluídos** - Lista de todos processos finalizados
2. **Processos em Andamento** - Processos ativos com status atual
3. **Análise por Empresa** - Consolidação por empresa
4. **Relatório Geral** - Visão consolidada com múltiplas abas

### Estrutura das Planilhas
- Dados de empresa (Nome, CNPJ)
- Informações do processo (ID, Nome, Status)
- Datas (Início, Conclusão, Previsão)
- Análises (Dias corridos, Passo atual, Porcentagem)

## 🔧 Configurações

Edite `config/config.json` para:
- Ajustar rate limit
- Definir processos a monitorar
- Configurar formato de saída
- Personalizar logs

## 📝 Próximos Passos

1. Documentar estrutura completa do processo "Simples Nacional - Mensal"
2. Implementar lógica de análise de passos
3. Desenvolver exportação para Excel
4. Criar análises e métricas
5. Testar com dados reais

## 🤝 Contribuindo

Este é um projeto interno. Para sugestões ou melhorias, entre em contato.

## 📄 Licença

Uso interno - Acessórias

---

**Última atualização:** 17 de Novembro de 2025
