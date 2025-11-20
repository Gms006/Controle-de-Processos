# 🤖 PROMPT PARA AGENTE IA - Análise de Erro Evolution API

---

## 📋 CONTEXTO

Estou tentando conectar o WhatsApp ao **Evolution API v2.0.10** (rodando em Docker no Windows) mas a conexão falha com erro **"stream error code 515"**.

---

## 🎯 MISSÃO

Analise os arquivos fornecidos e pesquise na documentação oficial da Evolution API para:

1. **Identificar a causa do erro "stream:error code 515"**
2. **Encontrar solução documentada ou workaround**
3. **Verificar se há configurações faltando no docker-compose.yml**
4. **Sugerir alternativas testadas pela comunidade**

---

## 📁 ARQUIVOS PARA ANÁLISE

### 1. ERRO_EVOLUTION_API.md
Contém:
- Descrição completa do erro
- Logs do Docker
- Tentativas realizadas
- Comportamento observado
- Status da instância

### 2. docker-compose.yml (Evolution API)
Configuração atual dos containers:
- Evolution API v2.0.10
- PostgreSQL 15-alpine
- Redis 7-alpine

### 3. Scripts PowerShell
- `conectar_whatsapp.ps1` - Script de conexão
- `webhook_simples.ps1` - Configuração webhook

---

## 🔍 PESQUISA NECESSÁRIA

### Fontes Oficiais
1. **GitHub Issues:** https://github.com/EvolutionAPI/evolution-api/issues
   - Buscar: "stream error 515", "code 515", "baileys connection failed"
   - Filtrar: Issues fechadas com solução

2. **Documentação:** https://doc.evolution-api.com/
   - Seção de troubleshooting
   - Configurações de ambiente
   - Requisitos de rede/firewall

3. **Discord/Community:**
   - Erros comuns e soluções
   - Configurações recomendadas para Windows/WSL2

### Questões-Chave

**Q1:** O que significa especificamente o erro "stream:error code 515" no contexto Baileys/WhatsApp?

**Q2:** Existem variáveis de ambiente obrigatórias faltando no docker-compose.yml?

**Q3:** A versão v2.0.10 do Evolution API tem bugs conhecidos de conexão?

**Q4:** Configurações de rede/proxy necessárias para Windows + Docker + WSL2?

**Q5:** Alternativas ao WHATSAPP-BAILEYS que funcionam melhor?

---

## ✅ O QUE ESTÁ FUNCIONANDO

- ✅ Docker containers estão rodando (healthy)
- ✅ Backend FastAPI respondendo (localhost:8000)
- ✅ QR Code é gerado corretamente
- ✅ Webhook configurado com sucesso
- ✅ WhatsApp Web normal funciona (web.whatsapp.com)
- ✅ API responde a requisições

---

## ❌ O QUE NÃO FUNCIONA

- ❌ Conexão WhatsApp via QR Code (erro 515)
- ❌ Pairing Code não é gerado
- ❌ Status fica "connecting" indefinidamente
- ❌ Erro persiste mesmo com números diferentes
- ❌ Erro persiste mesmo com WhatsApp pessoal (não business)

---

## 🎯 RESULTADO ESPERADO

Forneça:

1. **Diagnóstico:** Causa raiz do erro 515
2. **Solução:** Passo a passo para corrigir
3. **Código:** Mudanças necessárias (docker-compose.yml, variáveis, etc)
4. **Alternativas:** Se Evolution API não funcionar, outras APIs similares

---

## 📊 DADOS TÉCNICOS

```yaml
Sistema: Windows + Docker Desktop + WSL2
Evolution API: v2.0.10 (atendai/evolution-api)
Baileys Version: 2,3000,1027934701
Browser: Evolution API,Chrome,5.15.167.4-microsoft-standard-WSL2
PostgreSQL: 15-alpine
Redis: 7-alpine
API Key: acessorias_evolution_key_2025
```

---

## 🔗 LINKS IMPORTANTES

- Repositório: https://github.com/EvolutionAPI/evolution-api
- Documentação: https://doc.evolution-api.com/
- Issues: https://github.com/EvolutionAPI/evolution-api/issues
- Docker Hub: https://hub.docker.com/r/atendai/evolution-api

---

## ⚠️ IMPORTANTE

- NÃO é problema de banimento (testado com múltiplos números)
- NÃO é problema do QR Code (é gerado corretamente)
- NÃO é problema do WhatsApp (web.whatsapp.com funciona)
- É ESPECIFICAMENTE um problema de conexão entre Evolution API e WhatsApp

---

**ANALISE OS ARQUIVOS E RETORNE COM A SOLUÇÃO DEFINITIVA! 🚀**
