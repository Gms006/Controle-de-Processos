# 🚀 CONFIGURAÇÃO FINAL - WhatsApp Real

## ✅ O QUE JÁ ESTÁ PRONTO:

1. ✅ Backend rodando (localhost:8000)
2. ✅ Webhook funcionando 100%
3. ✅ Credenciais configuradas
4. ✅ Testes passando

---

## 🌐 PASSO 1: Expor Webhook Publicamente

### **Opção A: ngrok (Recomendado)**

```powershell
# Já instalamos! Agora execute:
cd "$env:USERPROFILE\ngrok"
.\ngrok.exe http 8000
```

**Você verá algo assim:**
```
ngrok

Session Status                online
Forwarding                    https://abc123.ngrok.io -> http://localhost:8000
```

**COPIE** a URL `https://abc123.ngrok.io` (a sua será diferente!)

---

### **Opção B: Localtunnel (Alternativa)**

```powershell
# Se tiver Node.js instalado:
npm install -g localtunnel
lt --port 8000
```

---

## ⚙️ PASSO 2: Configurar no Meta for Developers

### **1. Acessar Configurações**
```
https://developers.facebook.com/apps/
→ Seu App
→ WhatsApp
→ Configuration (Configuração)
```

### **2. Configurar Webhook**

Clique em **"Edit"** (Editar) na seção **Webhook**:

| Campo | Valor |
|-------|-------|
| **Callback URL** | `https://SUA_URL_NGROK.ngrok.io/whatsapp/webhook/whatsapp` |
| **Verify Token** | `acessorias_gestor_2025_token_secreto` |

**Exemplo:**
```
Callback URL: https://a1b2c3.ngrok.io/whatsapp/webhook/whatsapp
Verify Token: acessorias_gestor_2025_token_secreto
```

### **3. Subscribe to Webhook Fields**

Marque:
- ✅ **messages**

Clique em **"Verify and Save"** (Verificar e Salvar)

**Se aparecer ✅ verde, funcionou!**

---

## 📱 PASSO 3: Adicionar Número de Teste

### **No Meta for Developers:**

```
WhatsApp → API Setup
→ To: (Para)
→ Manage phone number list
→ Add phone number
```

**Digite:** `+5562992731445` (seu número)

**Você receberá um código via WhatsApp para confirmar**

---

## 🎉 PASSO 4: TESTAR!

### **No seu WhatsApp:**

1. **Abra o WhatsApp**
2. **Nova conversa** com: `+1 555-634-4237`
3. **Digite:** `0`

### **Você vai receber:**

```
╔═════════════════════════════════════╗
║   🤖 GESTOR DE PROCESSOS CONTÁBEIS   ║
╚═════════════════════════════════════╝
       Competência: 10/2025

📊 RESUMOS EXECUTIVOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1️⃣ Resumo Geral (KPIs principais)
2️⃣ Resumo por Regime Tributário
...
```

---

## 🧪 TESTE ANTES DE CONFIGURAR

Antes de ir ao Meta, teste se o ngrok está funcionando:

```powershell
# Obter URL do ngrok
Invoke-RestMethod -Uri "http://localhost:4040/api/tunnels" | 
  Select-Object -ExpandProperty tunnels | 
  Select-Object -ExpandProperty public_url
```

**Testar webhook:**
```powershell
# Substitua XXXX pela URL do ngrok
curl "https://XXXX.ngrok.io/whatsapp/webhook/whatsapp?hub.mode=subscribe&hub.verify_token=acessorias_gestor_2025_token_secreto&hub.challenge=TESTE"

# Deve retornar: TESTE
```

---

## 📊 MONITORAR MENSAGENS

No terminal onde rodou `python run.py`, você verá:

```
INFO: POST /whatsapp/webhook/whatsapp
📥 Mensagem de +5562992731445: "1"
✅ Comando: resumo_geral
📤 Enviando resposta (1234 caracteres)
```

---

## 🐛 TROUBLESHOOTING

### **Erro: "Verify Token Mismatch"**
- Verifique se copiou o token certo
- Token: `acessorias_gestor_2025_token_secreto`

### **Erro: "URL not accessible"**
- Verifique se ngrok está rodando
- Verifique se backend está rodando (localhost:8000)
- Teste a URL manualmente no navegador

### **Mensagem não chega**
- Verifique se seu número está na lista de teste
- Veja logs do backend
- Veja interface do ngrok: http://localhost:4040

### **Resposta não volta**
- Verifique se marcou "messages" no webhook
- Veja logs do backend para ver o erro

---

## 🎯 CHECKLIST FINAL

```
[✅] Backend rodando
[✅] Webhook testado localmente
[⏳] ngrok rodando (execute agora!)
[⏳] URL pública copiada
[⏳] Webhook configurado no Meta
[⏳] Número de teste adicionado
[⏳] Primeira mensagem enviada!
```

---

## 🚀 EXECUTE AGORA:

### **Terminal 1: Backend**
```powershell
cd "c:\acessorias processos\backend"
python run.py
```

### **Terminal 2: ngrok**
```powershell
cd "$env:USERPROFILE\ngrok"
.\ngrok.exe http 8000
```

### **Depois:**
1. Copie a URL do ngrok
2. Configure no Meta for Developers
3. Envie mensagem no WhatsApp!

---

**Quer que eu te ajude a configurar agora?** 📱
