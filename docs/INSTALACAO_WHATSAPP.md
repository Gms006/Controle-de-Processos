# 🚀 GUIA DE INSTALAÇÃO E CONFIGURAÇÃO
## Gestor de Processos via WhatsApp - 100% Gratuito

---

## 📋 PRÉ-REQUISITOS

### Software Necessário:

1. **Python 3.10+**
   - Download: https://www.python.org/downloads/

2. **Git** (opcional)
   - Download: https://git-scm.com/downloads

3. **Conta WhatsApp Business** (gratuita)
   - Download app: Google Play Store / Apple Store

### Conhecimentos Básicos:

- ✅ Executar comandos no terminal/PowerShell
- ✅ Editar arquivos de configuração (.env)
- ⚠️ Opcional: Conceitos básicos de API REST

---

## 🔧 INSTALAÇÃO PASSO A PASSO

### Passo 1: Preparar Ambiente Python

```powershell
# Navegar para o diretório do projeto
cd "c:\acessorias processos"

# Criar ambiente virtual (se ainda não existe)
python -m venv venv

# Ativar ambiente virtual
.\venv\Scripts\Activate.ps1

# Instalar dependências
pip install -r requirements.txt

# Instalar dependências do WhatsApp
pip install requests python-dotenv
```

### Passo 2: Configurar Variáveis de Ambiente

Criar arquivo `.env` na raiz do projeto:

```powershell
# Copiar exemplo
copy .env.example .env

# Editar .env
notepad .env
```

Conteúdo do `.env`:

```env
# ============ BANCO DE DADOS ============
DATABASE_URL=sqlite:///./database.db

# ============ WHATSAPP BUSINESS API ============
# Token de verificação do webhook (escolha um aleatório)
WHATSAPP_VERIFY_TOKEN=acessorias_token_2025_meu_secret

# App Secret (Meta Cloud API)
WHATSAPP_APP_SECRET=seu_app_secret_aqui

# Access Token (Meta Cloud API)
WHATSAPP_ACCESS_TOKEN=seu_access_token_aqui

# Phone Number ID (Meta Cloud API)
WHATSAPP_PHONE_NUMBER_ID=seu_phone_id_aqui

# ============ GESTORES AUTORIZADOS ============
# Números de telefone autorizados (separados por vírgula)
# Formato: +5511999999999,+5511888888888
GESTORES_AUTORIZADOS=+5511999999999

# ============ CONFIGURAÇÕES GERAIS ============
COMPETENCIA_PADRAO=10/2025
```

### Passo 3: Verificar Banco de Dados

```powershell
# Verificar se banco tem dados
python scripts/verificar_banco.py

# Resultado esperado:
# 📊 Total de processos: 62
# 📋 Por regime:
#    Lucro Presumido: 44 empresas
#    Lucro Real: 17 empresas
```

Se não houver dados, sincronizar:

```powershell
# Sincronizar dados da API Acessórias
cd backend
python -m app.services.acessorias_sync
```

---

## 📱 CONFIGURAÇÃO DO WHATSAPP

### Opção 1: Meta Cloud API (RECOMENDADO - Gratuito)

**Vantagens:**
- ✅ 1.000 conversas gratuitas/mês
- ✅ Oficial do Meta/Facebook
- ✅ Confiável e escalável

**Desvantagens:**
- ⚠️ Configuração mais complexa
- ⚠️ Requer verificação de negócio

**Passo a Passo:**

1. **Criar Conta no Meta for Developers**
   - Acesse: https://developers.facebook.com/
   - Faça login com Facebook
   - Clique em "My Apps" → "Create App"

2. **Configurar WhatsApp Business**
   - Escolha "Business" como tipo
   - Nome do app: "Gestor Processos Acessorias"
   - Adicione produto "WhatsApp"

3. **Obter Credenciais**
   - Acesse WhatsApp → API Setup
   - Copie:
     - **Phone Number ID** (coloque no `.env`)
     - **WhatsApp Business Account ID**
     - **Access Token** (temporário - gere permanente depois)

4. **Gerar Token Permanente**
   - Acesse "Business Settings" → "System Users"
   - Crie system user
   - Gere token com permissões: `whatsapp_business_messaging`, `whatsapp_business_management`
   - Copie token e salve no `.env`

5. **Configurar Webhook**
   - Na seção "Configuration"
   - Webhook URL: `https://seu-dominio.com/webhook/whatsapp`
   - Verify Token: O mesmo que você colocou no `.env`
   - Subscribe to: `messages`

6. **Expor Webhook Publicamente**
   
   **Opção A: Ngrok (Desenvolvimento)**
   ```powershell
   # Instalar ngrok
   # Download: https://ngrok.com/download
   
   # Executar backend
   cd backend
   python run.py
   
   # Em outro terminal, expor porta 8000
   ngrok http 8000
   
   # Copiar URL HTTPS (ex: https://abc123.ngrok.io)
   # Usar como Webhook URL: https://abc123.ngrok.io/webhook/whatsapp
   ```
   
   **Opção B: Servidor Próprio (Produção)**
   - Hospedar em Heroku, AWS, Google Cloud, etc.
   - Configurar domínio e SSL (HTTPS obrigatório)

### Opção 2: Evolution API (GRATUITO - Self-Hosted)

**Vantagens:**
- ✅ 100% Gratuito
- ✅ Sem limites de conversas
- ✅ Open source
- ✅ Fácil de configurar

**Desvantagens:**
- ⚠️ Requer servidor próprio
- ⚠️ Menos "oficial" que Meta API

**Passo a Passo:**

1. **Instalar Docker**
   - Download: https://www.docker.com/products/docker-desktop/

2. **Executar Evolution API**
   ```powershell
   # Baixar Evolution API
   docker pull atendai/evolution-api:latest
   
   # Executar
   docker run -d \
     -p 8080:8080 \
     -e AUTHENTICATION_API_KEY=minha_chave_secreta \
     atendai/evolution-api:latest
   ```

3. **Criar Instância WhatsApp**
   ```powershell
   # Via Postman ou curl
   curl -X POST http://localhost:8080/instance/create \
     -H "apikey: minha_chave_secreta" \
     -H "Content-Type: application/json" \
     -d '{
       "instanceName": "gestor-processos",
       "qrcode": true
     }'
   ```

4. **Conectar WhatsApp**
   - Acessar: http://localhost:8080/instance/qrcode/gestor-processos
   - Escanear QR Code com WhatsApp no celular
   - WhatsApp → Configurações → Aparelhos Conectados → Conectar Aparelho

5. **Configurar Webhook**
   ```powershell
   curl -X POST http://localhost:8080/webhook/set/gestor-processos \
     -H "apikey: minha_chave_secreta" \
     -H "Content-Type: application/json" \
     -d '{
       "webhook": "http://localhost:8000/webhook/whatsapp",
       "events": ["messages.upsert"]
     }'
   ```

### Opção 3: Twilio (PAGO)

**Custos:**
- 💰 $0.005 por mensagem recebida
- 💰 $0.005-$0.08 por mensagem enviada

**Não recomendado para uso gratuito.**

---

## 🚀 EXECUTAR O SISTEMA

### 1. Iniciar Backend FastAPI

```powershell
cd "c:\acessorias processos\backend"
python run.py
```

Saída esperada:
```
✅ Webhook WhatsApp configurado
INFO:     Started server process
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 2. Testar Webhook Localmente

Abra outro terminal:

```powershell
# Testar endpoint de status
curl http://localhost:8000/webhook/whatsapp/status

# Testar comando (desenvolvimento)
curl -X POST "http://localhost:8000/webhook/whatsapp/test?comando=1&telefone=%2B5511999999999"
```

### 3. Expor Publicamente (Ngrok)

```powershell
ngrok http 8000
```

Copie a URL HTTPS gerada e use no webhook do WhatsApp.

### 4. Enviar Primeira Mensagem

- Abra WhatsApp no celular
- Envie mensagem para o número configurado (Meta Cloud API)
  OU
- Envie mensagem para seu próprio número (Evolution API)

- Digite: `0` ou `menu`

Você deve receber o menu principal! 🎉

---

## 🔍 TESTES E VALIDAÇÃO

### Teste 1: Menu Principal

```
Enviar: 0
Esperar: Menu com 24 opções
```

### Teste 2: Resumo Geral

```
Enviar: 1
Esperar: Resumo com KPIs principais
```

### Teste 3: Busca de Empresa

```
Enviar: MOUSSA
Esperar: Detalhes da empresa MOUSSA CONSTRUTORA
```

### Teste 4: Comando Inválido

```
Enviar: xyz
Esperar: Mensagem de erro + instrução para menu
```

---

## 🐛 SOLUÇÃO DE PROBLEMAS

### Erro: "Telefone não autorizado"

**Solução:**
- Verifique `.env` → `GESTORES_AUTORIZADOS`
- Adicione seu número no formato: `+5511999999999`
- Reinicie o backend

### Erro: "Webhook não recebe mensagens"

**Solução:**
1. Verifique se backend está rodando:
   ```powershell
   curl http://localhost:8000/webhook/whatsapp/status
   ```

2. Verifique ngrok (se usando):
   ```powershell
   # Acessar painel
   http://127.0.0.1:4040
   ```

3. Verifique configuração do webhook no Meta/Evolution API

### Erro: "Banco de dados vazio"

**Solução:**
```powershell
# Sincronizar dados
cd backend
python -m app.services.acessorias_sync
```

### Erro: "Módulo não encontrado"

**Solução:**
```powershell
# Ativar ambiente virtual
.\venv\Scripts\Activate.ps1

# Reinstalar dependências
pip install -r requirements.txt
```

---

## 📊 MONITORAMENTO

### Logs do Backend

```powershell
# Logs em tempo real (stdout)
cd backend
python run.py

# Ver logs salvos
type logs/app.log
```

### Logs do WhatsApp

```powershell
# Comandos executados
type logs/whatsapp_commands.log
```

### Métricas de Uso

```powershell
# Quantos comandos foram executados hoje
python scripts/relatorio_uso_whatsapp.py
```

---

## 🔐 SEGURANÇA

### Recomendações:

1. **Nunca compartilhe tokens**
   - `.env` no `.gitignore`
   - Não commite tokens no Git

2. **Use HTTPS**
   - Webhook DEVE usar HTTPS
   - Certificado SSL válido

3. **Valide assinaturas**
   - Meta API: Verificar `X-Hub-Signature-256`
   - Implementado em `webhook.py`

4. **Limite acessos**
   - Apenas números autorizados
   - Rate limiting (implementar se necessário)

5. **Atualize dependências**
   ```powershell
   pip install --upgrade pip
   pip list --outdated
   ```

---

## 📚 PRÓXIMOS PASSOS

### Fase 1: Usar o Sistema ✅
- Configure WhatsApp
- Teste todos os comandos
- Familiarize-se com métricas

### Fase 2: Personalizar
- Adicione mais comandos em `processor.py`
- Customize relatórios em `formatador.py`
- Ajuste métricas em `analytics.py`

### Fase 3: Expandir
- Adicione alertas automáticos (agendados)
- Implemente notificações proativas
- Integre com outros sistemas

### Fase 4: Escalar
- Migre para servidor de produção
- Configure backup de banco de dados
- Implemente logs profissionais (Sentry, etc.)

---

## 💡 DICAS DE USO

### Para o Gestor:

1. **Comece com o comando "1"** (Resumo Geral)
   - Visão rápida de tudo

2. **Use "12"** (Empresas Paradas) diariamente
   - Identifique bloqueios rapidamente

3. **Busque empresas específicas**
   - Digite o nome direto
   - Ex: "MOUSSA"

4. **Salve comandos favoritos**
   - Anote números mais usados
   - Crie atalhos no WhatsApp

### Para Performance:

- ⚡ Comandos respondem em 1-3 segundos
- 📊 Dados atualizados em tempo real
- 💾 Cache automático para consultas repetidas

---

## 🆘 SUPORTE

### Documentação Adicional:

- `GESTOR_WHATSAPP_ESPECIFICACAO.md` - Especificação completa
- `backend/whatsapp/README.md` - Documentação técnica

### Contato:

- 📧 Email: seu_email@empresa.com
- 💬 WhatsApp: +55 11 99999-9999

---

**Última atualização:** 18/11/2025  
**Versão:** 1.0  
**Status:** Pronto para Produção ✅
