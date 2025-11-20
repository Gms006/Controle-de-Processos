# 🧪 TESTE LOCAL - WhatsApp Gestor

## ✅ STATUS: Backend Rodando!

```
✅ WhatsApp webhook importado com sucesso!
✅ WhatsApp Webhook registrado em /whatsapp
✅ Server: http://localhost:8000
```

---

## 📡 ENDPOINTS DISPONÍVEIS

### 1. **Webhook WhatsApp**
- **GET** `/whatsapp/webhook/whatsapp` - Verificação do webhook (Meta)
- **POST** `/whatsapp/webhook/whatsapp` - Receber mensagens

### 2. **Documentação**
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🧪 TESTE 1: Verificar Webhook (Simulação Meta)

```powershell
# Teste de verificação (GET)
curl "http://localhost:8000/whatsapp/webhook/whatsapp?hub.mode=subscribe&hub.verify_token=acessorias_gestor_2025_token_secreto&hub.challenge=teste123"
```

**Resposta esperada:** `teste123`

---

## 🧪 TESTE 2: Simular Mensagem do WhatsApp

```powershell
# Simular mensagem recebida
curl -X POST "http://localhost:8000/whatsapp/webhook/whatsapp" `
  -H "Content-Type: application/json" `
  -d '{
    "object": "whatsapp_business_account",
    "entry": [{
      "changes": [{
        "value": {
          "messages": [{
            "from": "5562992731445",
            "text": {
              "body": "0"
            }
          }]
        }
      }]
    }]
  }'
```

**O que acontece:**
1. ✅ Backend recebe mensagem
2. ✅ Identifica comando "0" (menu)
3. ✅ Gera resposta formatada
4. ✅ TENTA enviar via API do WhatsApp
5. ⚠️ Vai falhar (normal - ainda não configuramos webhook público)

---

## 🌐 PRÓXIMO PASSO: Webhook Público (ngrok)

Para o WhatsApp REAL funcionar, precisamos:

### **Opção 1: ngrok (Recomendado para Teste)**

```powershell
# 1. Instalar ngrok
choco install ngrok
# OU baixar: https://ngrok.com/download

# 2. Executar ngrok
ngrok http 8000
```

**Resultado:**
```
Forwarding  https://abc123.ngrok.io -> http://localhost:8000
```

### **Opção 2: Localtunnel (Alternativa Gratuita)**

```powershell
# 1. Instalar (precisa Node.js)
npm install -g localtunnel

# 2. Executar
lt --port 8000
```

---

## ⚙️ CONFIGURAR NO META FOR DEVELOPERS

Depois de ter a URL pública (ngrok ou localtunnel):

1. **Acesse:** https://developers.facebook.com/apps/
2. **Seu App** → **WhatsApp** → **Configuration**
3. **Webhook**:
   - Callback URL: `https://SEU_NGROK.ngrok.io/whatsapp/webhook/whatsapp`
   - Verify Token: `acessorias_gestor_2025_token_secreto`
4. **Subscribe to**:
   - ✅ messages
5. **Save**

---

## 📱 ENVIAR PRIMEIRA MENSAGEM!

1. **Abra WhatsApp** no seu celular (+5562992731445)
2. **Envie mensagem** para: `+1 555-634-4237`
3. **Digite:** `0`

**O sistema vai responder:**

```
╔══════════════════════════════╗
║   GESTOR DE PROCESSOS       ║
║   📊 Menu Principal         ║
╚══════════════════════════════╝

📌 RESUMOS EXECUTIVOS
1️⃣ Resumo Geral (KPIs)
2️⃣ Resumo por Regime
3️⃣ Resumo por Empresa

📊 ANÁLISES ESPECÍFICAS
4️⃣ Empresas sem Faturamento
5️⃣ Empresas com Tributos
...
```

---

## 🎯 COMANDOS DISPONÍVEIS

| Comando | Descrição |
|---------|-----------|
| `0` | Menu principal |
| `1` | Resumo geral (KPIs) |
| `4` | Empresas sem faturamento |
| `8` | Tempo de finalização |
| `12` | Empresas paradas |
| `20 [nome]` | Buscar empresa |

---

## 🐛 TROUBLESHOOTING

### **Erro: "Webhook não registrado"**
✅ **Resolvido!** Backend agora carrega webhook automaticamente

### **Erro: "No module named 'backend'"**
✅ **Resolvido!** Imports corrigidos

### **Mensagem não chega**
- Verifique se ngrok está rodando
- Verifique URL no Meta for Developers
- Veja logs do backend (terminal)

### **Resposta não volta**
- Normal! Webhook precisa estar configurado no Meta
- Por enquanto, veja a resposta nos logs do backend

---

## 📊 MONITORAR LOGS

No terminal onde rodou `python run.py`, você verá:

```
INFO: POST /whatsapp/webhook/whatsapp
✅ Mensagem recebida de +5562992731445
✅ Comando identificado: menu
✅ Resposta gerada (1234 caracteres)
⚠️  Erro ao enviar (esperado sem webhook público)
```

---

## ✅ CHECKLIST COMPLETO

```
[✅] Backend rodando
[✅] Webhook registrado
[✅] Credenciais configuradas (.env)
[✅] Documentação acessível
[⏳] ngrok/localtunnel (próximo)
[⏳] Configurar no Meta
[⏳] Primeiro teste real
```

---

## 🚀 QUER TESTAR AGORA?

**Execute um destes comandos no PowerShell:**

### Teste de Verificação:
```powershell
curl "http://localhost:8000/whatsapp/webhook/whatsapp?hub.mode=subscribe&hub.verify_token=acessorias_gestor_2025_token_secreto&hub.challenge=TESTE"
```

### Teste de Mensagem:
```powershell
$body = @{
    object = "whatsapp_business_account"
    entry = @(
        @{
            changes = @(
                @{
                    value = @{
                        messages = @(
                            @{
                                from = "5562992731445"
                                text = @{
                                    body = "1"
                                }
                            }
                        )
                    }
                }
            )
        }
    )
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Method Post -Uri "http://localhost:8000/whatsapp/webhook/whatsapp" -Body $body -ContentType "application/json"
```

---

**Quer testar localmente antes de configurar ngrok?** 🧪
