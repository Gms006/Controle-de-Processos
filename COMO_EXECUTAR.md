# 🚀 GUIA DE EXECUÇÃO RÁPIDA

## ✅ Pré-requisitos

1. ✓ Python 3.8+ instalado
2. ✓ Arquivo `.env` configurado com seu `API_TOKEN`

---

## 📋 Passo a Passo

### 1️⃣ Configurar ambiente (apenas primeira vez)

```powershell
# Navegar para o diretório
cd "c:\acessorias processos"

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
.\venv\Scripts\Activate

# Instalar dependências
pip install -r requirements.txt
```

### 2️⃣ Configurar credenciais

```powershell
# Se ainda não criou o .env
copy .env.example .env

# Editar e adicionar seu token
notepad .env
```

No arquivo `.env`, adicione:
```
API_TOKEN=seu_token_real_aqui
```

### 3️⃣ Executar o script

```powershell
# Certificar-se que o ambiente virtual está ativo
.\venv\Scripts\Activate

# Executar
python scripts\buscar_processos_simples_nacional.py
```

---

## 📊 O que o script faz:

1. **Conecta à API** Acessórias
2. **Busca processos** do Simples Nacional:
   - Processos em andamento (status A)
   - Processos concluídos (status C)
3. **Processa os dados**:
   - Extrai informações gerais
   - Analisa todos os passos
   - Identifica desdobramentos
4. **Gera planilha Excel** com 3 abas:
   - PROCESSOS_GERAL
   - PROCESSOS_PASSOS
   - PROCESSOS_DESDOBRAMENTOS
5. **Salva backup** dos dados brutos em JSON

---

## 📁 Arquivos Gerados

### Planilha Excel:
```
output/planilhas/SimplesNacional_DadosBrutos_YYYYMMDD_HHMMSS.xlsx
```

### Backup JSON:
```
data/raw/processos_YYYYMMDD_HHMMSS.json
```

### Logs:
```
logs/app.log
```

---

## 🔍 Validar Resultados

Após a execução, abra a planilha e verifique:

### ✅ Aba 1: PROCESSOS_GERAL
- [ ] Total de processos está correto?
- [ ] Nomes de empresas aparecem?
- [ ] Datas estão preenchidas?
- [ ] Status está correto (Concluído/Em andamento)?

### ✅ Aba 2: PROCESSOS_PASSOS
- [ ] Cada processo tem seus passos listados?
- [ ] Ordem dos passos faz sentido?
- [ ] Tipos de passos estão corretos?
- [ ] Responsáveis aparecem?

### ✅ Aba 3: PROCESSOS_DESDOBRAMENTOS
- [ ] Desdobramentos (decisões) aparecem?
- [ ] Alternativas disponíveis estão listadas?
- [ ] Consegue identificar decisões tomadas?

---

## 🐛 Troubleshooting

### Erro: "API_TOKEN não configurado"
**Solução:** Edite o arquivo `.env` e adicione seu token real

### Erro: "Import não encontrado"
**Solução:** 
```powershell
.\venv\Scripts\Activate
pip install -r requirements.txt
```

### Erro: "Nenhum processo encontrado"
**Possíveis causas:**
1. Token inválido
2. Não existem processos de Simples Nacional no sistema
3. Sem permissão para acessar processos

**Verificar:**
```powershell
# Ver logs detalhados
type logs\app.log
```

### Erro de conexão/timeout
**Solução:** Verifique sua conexão com internet e tente novamente

---

## 📧 Feedback

Após validar a planilha, me informe:

✅ **O que está correto:**
- Dados sendo extraídos corretamente?
- Estrutura faz sentido?

⚠️ **O que precisa ajustar:**
- Algum campo faltando?
- Algum dado incorreto?
- Alguma análise adicional?

🚀 **Próximos passos:**
- Implementar abas de gestão (Dashboard, Alertas, Ranking)?
- Adicionar mais filtros?
- Outras análises?

---

## ⚡ Execuções Futuras

Após a primeira configuração, basta executar:

```powershell
cd "c:\acessorias processos"
.\venv\Scripts\Activate
python scripts\buscar_processos_simples_nacional.py
```

**Simples assim!** 🎉
