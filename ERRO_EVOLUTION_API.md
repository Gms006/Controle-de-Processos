# 🔴 ERRO: Evolution API - Stream Error Code 515

## 📋 Resumo do Problema

Estamos tentando conectar o WhatsApp ao Evolution API v2.0.10 via Docker, mas a conexão falha consistentemente com o erro **"stream error code 515"**.

---

## 🔧 Ambiente Técnico

### Infraestrutura
- **Sistema Operacional:** Windows
- **Docker Desktop:** Instalado e funcionando
- **Evolution API:** v2.0.10 (container Docker)
- **PostgreSQL:** 15-alpine (container Docker)
- **Redis:** 7-alpine (container Docker)
- **Backend:** Python FastAPI (localhost:8000)
- **Integration:** WHATSAPP-BAILEYS

### Containers Ativos
```
evolution_api        atendai/evolution-api:v2.0.10   Up 15 minutes   0.0.0.0:8081->8080/tcp
evolution_postgres   postgres:15-alpine              Up 15 minutes   5432/tcp
evolution_redis      redis:7-alpine                  Up 15 minutes   6379/tcp
```

---

## ❌ Erro Detalhado

### Log do Docker (evolution_api)
```
{"level":50,"time":1763512278361,"pid":178,"hostname":"767b0cb38cd7","node":{"tag":"stream:error","attrs":{"code":"515"}},"msg":"stream errored out"}
```

### Comportamento Observado
1. ✅ QR Code é gerado corretamente
2. ✅ QR Code é exibido no navegador
3. ✅ Usuário escaneia o QR Code com WhatsApp
4. ❌ Conexão falha com erro "stream:error code 515"
5. 🔄 Status permanece em "connecting" indefinidamente
6. ❌ Após ~10 segundos, QR Code expira e processo reinicia

### Tentativas Realizadas

#### Tentativa 1: QR Code Normal
```powershell
$body = @{
    instanceName="acessorias"
    qrcode=$true
    integration="WHATSAPP-BAILEYS"
} | ConvertTo-Json
```
**Resultado:** Erro 515

#### Tentativa 2: Pairing Code (Código de Pareamento)
```powershell
$body = @{
    instanceName="acessorias"
    number="5562999976999"
    integration="WHATSAPP-BAILEYS"
} | ConvertTo-Json
```
**Resultado:** Não gerou pairing code (retornou apenas status "created")

#### Tentativa 3: QR Code + Webhook Pré-configurado
```powershell
$body = @{
    instanceName="acessorias"
    qrcode=$true
    integration="WHATSAPP-BAILEYS"
    webhook=@{
        enabled=$true
        url="http://localhost:8000/whatsapp/evolution/webhook"
        webhookByEvents=$false
        webhookBase64=$false
        events=@("MESSAGES_UPSERT","CONNECTION_UPDATE")
    }
} | ConvertTo-Json -Depth 10
```
**Resultado:** Erro 515

#### Tentativa 4: Reiniciar Containers
```powershell
docker-compose restart
```
**Resultado:** Erro persiste

#### Tentativa 5: Testar com WhatsApp Pessoal (não Business)
**Resultado:** Mesmo erro 515

---

## 🔍 Observações Importantes

### Confirmações
- ✅ WhatsApp Web **normal** funciona perfeitamente (web.whatsapp.com)
- ✅ Backend FastAPI está rodando corretamente (localhost:8000)
- ✅ Webhook foi configurado com sucesso via API
- ✅ Docker containers estão healthy
- ✅ Logs mostram que Baileys version é: `2,3000,1027934701`
- ✅ Browser identificado: `Evolution API,Chrome,5.15.167.4-microsoft-standard-WSL2`

### Problemas Conhecidos
- ❌ Número WhatsApp Business (62 99997-6999) estava em conta **banida** pela Meta
- ❌ Testado com número WhatsApp pessoal diferente - **mesmo erro**
- ❌ Erro **não é relacionado ao banimento** (persiste com números limpos)

---

## 📁 Arquivos Relevantes

### 1. docker-compose.yml
Localização: `C:\acessorias processos\evolution-api\docker-compose.yml`

### 2. Script de Conexão (conectar_whatsapp.ps1)
Localização: `C:\acessorias processos\conectar_whatsapp.ps1`

Função:
- Deleta instância antiga
- Cria nova instância com QR Code
- Gera HTML com QR Code embutido
- Abre no navegador

### 3. Script de Configuração Webhook (webhook_simples.ps1)
Localização: `C:\acessorias processos\webhook_simples.ps1`

Função:
- Configura webhook na instância
- Valida configuração

### 4. Backend WhatsApp Processor
Localização: `C:\acessorias processos\backend\whatsapp\processor.py`

24 comandos implementados para análise de processos contábeis.

---

## 🔎 Pesquisas Necessárias

### Questões Principais

1. **O que significa "stream error code 515" no contexto Baileys/WhatsApp Web?**
   - Documentação oficial: https://github.com/EvolutionAPI/evolution-api
   - Issues GitHub relacionadas ao erro 515
   - Problemas conhecidos com Baileys v6.x

2. **Configurações faltantes ou incorretas?**
   - Variáveis de ambiente necessárias
   - Permissões de rede/firewall
   - Configurações WSL2 para Docker no Windows

3. **Versão incompatível?**
   - Evolution API v2.0.10 tem bugs conhecidos?
   - Baileys precisa de downgrade?
   - PostgreSQL/Redis configurados corretamente?

4. **Alternativas testadas pela comunidade?**
   - Usar INTEGRATION diferente (não WHATSAPP-BAILEYS)?
   - Configurações adicionais necessárias?
   - Workarounds documentados?

---

## 📊 Status da Instância

```json
{
  "id": "88c58866-c534-4f4f-98f8-17486965883f",
  "name": "acessorias",
  "connectionStatus": "connecting",
  "ownerJid": null,
  "profileName": null,
  "integration": "WHATSAPP-BAILEYS",
  "number": null,
  "token": "F3E753C1-58A4-4713-ADE6-D5DA0BE65D72",
  "disconnectionReasonCode": null,
  "disconnectionAt": null
}
```

**Nota:** Status nunca muda de "connecting" para "open"

---

## 🎯 Objetivo Final

Conectar WhatsApp (pessoal ou business) ao Evolution API para:
- Receber mensagens via webhook
- Processar comandos automaticamente
- Enviar respostas com análises contábeis

---

## 📝 Comandos para Reproduzir o Erro

```powershell
# 1. Iniciar Docker
cd 'C:\acessorias processos\evolution-api'
docker-compose up -d

# 2. Iniciar Backend
cd 'C:\acessorias processos\backend'
python run.py

# 3. Gerar QR Code e tentar conectar
cd 'C:\acessorias processos'
.\conectar_whatsapp.ps1

# 4. Verificar logs do erro
docker logs evolution_api --tail=50

# 5. Verificar status
Invoke-RestMethod -Uri "http://localhost:8081/instance/fetchInstances?instanceName=acessorias" -Headers @{"apikey"="acessorias_evolution_key_2025"}
```

---

## 💡 Hipóteses a Investigar

1. **Problema de proxy/tunnel:** WhatsApp pode estar bloqueando conexões de WSL2/Docker
2. **Configuração de rede:** Falta configurar variáveis de ambiente de rede
3. **Bug da versão:** Evolution API v2.0.10 pode ter bug conhecido
4. **Baileys desatualizado:** Versão do Baileys incompatível com protocolos atuais do WhatsApp
5. **Firewall Windows:** Bloqueando comunicação WebSocket

---

## 🔗 Links Úteis

- Evolution API GitHub: https://github.com/EvolutionAPI/evolution-api
- Documentação: https://doc.evolution-api.com/
- Issues: https://github.com/EvolutionAPI/evolution-api/issues
- Discord/Suporte: https://evolution-api.com/discord
