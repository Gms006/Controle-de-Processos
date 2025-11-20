# 🎯 GUIA RÁPIDO: WhatsApp via Evolution API

## ✅ O QUE JÁ ESTÁ FUNCIONANDO

### Backend Python + WhatsApp
- ✅ Backend FastAPI rodando (localhost:8000)
- ✅ 24 comandos WhatsApp implementados
- ✅ Sistema completo de analytics (empresas, tributos, tempo finalização, etc)
- ✅ Formatação mobile otimizada
- ✅ Webhook Evolution API configurado (`/whatsapp/evolution/webhook`)

### Docker Evolution API
- ✅ Evolution API v2.0.10 instalado e rodando (localhost:8081)
- ✅ PostgreSQL healthy
- ✅ Redis conectado
- ✅ Containers: `evolution_api`, `evolution_postgres`, `evolution_redis`

### Credenciais
- API Key: `acessorias_evolution_key_2025`
- WhatsApp Business: **62 99997-6999** (número a ser conectado)
- Gestor autorizado: +5562992731445

---

## 🚀 CONECTAR WHATSAPP AGORA (3 PASSOS)

### PASSO 1: Gerar QR Code
Execute no PowerShell:

```powershell
$body = @{
  instanceName="acessorias"
  qrcode=$true
  integration="WHATSAPP-BAILEYS"
  webhook=@{
    url="http://localhost:8000/whatsapp/evolution/webhook"
    enabled=$true
    webhookByEvents=$false
    webhookBase64=$true
    events=@("QRCODE_UPDATED","CONNECTION_UPDATE","MESSAGES_UPSERT")
  }
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Uri "http://localhost:8081/instance/create" -Method POST -Headers @{"Content-Type"="application/json"; "apikey"="acessorias_evolution_key_2025"} -Body $body | ConvertTo-Json -Depth 10
```

**Resultado esperado:**
```json
{
  "qrcode": {
    "base64": "data:image/png;base64,iVBORw0KG...",
    "code": "2@Sz8jWO...",
    "count": 1
  }
}
```

### PASSO 2: Escanear QR Code
1. **Copie** o valor do campo `"base64"` (toda a string que começa com `data:image/png;base64,`)
2. **Cole** na barra de endereço do navegador
3. O QR Code aparecerá na tela

### PASSO 3: Conectar WhatsApp Business
1. Abra **WhatsApp Business** no celular (62 99997-6999)
2. Toque **⋮** (três pontos) → **Aparelhos conectados**
3. Toque **Conectar aparelho**
4. **Escaneie** o QR Code do navegador

---

## 📱 COMO USAR APÓS CONECTAR

### Comandos Disponíveis
Envie mensagem para o WhatsApp Business conectado:

- `0` ou `menu` → Menu completo
- `1` → Resumo geral (KPIs)
- `4` → Empresas sem faturamento
- `8` → Tempo de finalização
- `20 nome` → Buscar empresa por nome
- ... (24 comandos no total)

### Verificar Conexão
```powershell
Invoke-RestMethod -Uri "http://localhost:8081/instance/fetchInstances?instanceName=acessorias" -Headers @{"apikey"="acessorias_evolution_key_2025"} | ConvertTo-Json -Depth 10
```

**Status esperado após conexão:**
```json
{
  "connectionStatus": "open",
  "ownerJid": "5562999976999@s.whatsapp.net"
}
```

---

## 🔧 TROUBLESHOOTING

### Se QR Code expirar (após 40s)
```powershell
# Deletar instância antiga
Invoke-RestMethod -Uri "http://localhost:8081/instance/delete/acessorias" -Method DELETE -Headers @{"apikey"="acessorias_evolution_key_2025"}

# Recriar (execute PASSO 1 novamente)
```

### Se instância já existir
```powershell
# Verificar instâncias
Invoke-RestMethod -Uri "http://localhost:8081/instance/fetchInstances" -Headers @{"apikey"="acessorias_evolution_key_2025"}

# Deletar se necessário
Invoke-RestMethod -Uri "http://localhost:8081/instance/delete/acessorias" -Method DELETE -Headers @{"apikey"="acessorias_evolution_key_2025"}
```

### Reiniciar containers se necessário
```powershell
cd 'c:\acessorias processos\evolution-api'
docker-compose restart
```

---

## 📂 ARQUIVOS IMPORTANTES

### Docker Compose
`c:\acessorias processos\evolution-api\docker-compose.yml`
- Evolution API v2.0.10
- PostgreSQL 15-alpine
- Redis 7-alpine

### Backend
- `backend/app/routers/evolution.py` → Webhook Evolution
- `backend/whatsapp/processor.py` → Processador de comandos (24 comandos)
- `backend/whatsapp/analytics.py` → Analytics e métricas
- `backend/whatsapp/formatador.py` → Formatação mobile

### Banco de Dados
- `backend/database.db` → SQLite com todos os processos

---

## 🎯 PRÓXIMOS PASSOS APÓS CONECTAR

1. **Testar comando básico:** Envie `0` para o WhatsApp
2. **Validar resposta:** Sistema deve retornar menu completo
3. **Testar analytics:** `1` (resumo geral), `4` (sem faturamento)
4. **Buscar empresa:** `20 nome da empresa`

---

## ⚙️ COMANDOS ÚTEIS

### Ver logs Evolution API
```powershell
docker logs evolution_api --tail 50
```

### Ver status containers
```powershell
docker ps
```

### Restart backend
```powershell
cd 'c:\acessorias processos\backend'
python run.py
```

---

## 🔑 RESUMO TÉCNICO

**Sistema:** Gestor de Processos Contábeis via WhatsApp  
**Stack:** Python 3.14, FastAPI, Evolution API v2.0.10, Docker, PostgreSQL, Redis  
**Objetivo:** 100% gratuito, sem enviar mensagens (apenas receber e responder)  
**Analytics:** 24 comandos (resumos, métricas, buscas, indicadores)  
**Status atual:** 99% completo - falta apenas escanear QR Code

**Última tentativa de QR Code:** Gerado com sucesso em base64, pronto para escanear
