# 📱 GESTOR DE PROCESSOS CONTÁBEIS VIA WHATSAPP
## Sistema Completo de Gestão e Análise - 100% Gratuito

---

## 🎯 VISÃO GERAL

Sistema inteligente para gestão de processos contábeis com interface via **WhatsApp Business API**, permitindo ao gestor consultar métricas, identificar gargalos e buscar empresas diretamente pelo celular - **sem custos de envio de mensagens** (apenas recebe comandos).

### Principais Funcionalidades:

✅ **24 Comandos de Análise**
- Resumos executivos
- Análises por regime tributário
- Empresas sem faturamento
- Declarações pendentes
- Empresas paradas (0% progresso)
- Gargalos identificados
- Busca de empresas

✅ **Análises em Tempo Real**
- Dados atualizados do banco SQLite
- Métricas calculadas instantaneamente
- Insights automáticos

✅ **Interface Mobile-Friendly**
- Formatação otimizada para WhatsApp
- Emojis e barras de progresso
- Respostas em 1-3 segundos

✅ **100% Gratuito**
- Apenas recebe comandos (sem envio automático)
- Usa Meta Cloud API (1.000 conversas/mês grátis)
- Ou Evolution API (totalmente gratuito)

---

## 📁 ESTRUTURA DO PROJETO

```
c:\acessorias processos\
├── backend/                    # Backend FastAPI
│   ├── app/
│   │   ├── main.py            # Aplicação principal
│   │   ├── models/            # Modelos SQLAlchemy
│   │   ├── schemas/           # Schemas Pydantic
│   │   └── services/          # Serviços (sync, etc)
│   └── whatsapp/              # 🆕 MÓDULO WHATSAPP
│       ├── analytics.py       # Análise de dados e KPIs
│       ├── formatador.py      # Formatação de mensagens
│       ├── processor.py       # Processamento de comandos
│       └── webhook.py         # Webhook WhatsApp API
│
├── docs/                       # Documentação
│   ├── GESTOR_WHATSAPP_ESPECIFICACAO.md  # 🆕 Especificação completa
│   ├── INSTALACAO_WHATSAPP.md            # 🆕 Guia de instalação
│   ├── COMANDOS_WHATSAPP.md              # 🆕 Lista de comandos
│   └── ...
│
├── scripts/                    # Scripts Python
│   ├── sincronizar_banco.py   # Sincronização com API
│   ├── verificar_banco.py     # Verificar dados
│   └── ...
│
├── database.db                 # Banco de dados SQLite
├── requirements.txt            # Dependências Python
└── .env                        # Configurações (criar)
```

---

## 🚀 INÍCIO RÁPIDO

### 1. Instalar Dependências

```powershell
cd "c:\acessorias processos"
pip install -r requirements.txt
```

### 2. Configurar Ambiente

```powershell
# Copiar exemplo
copy .env.example .env

# Editar .env
notepad .env
```

Adicione no `.env`:
```env
WHATSAPP_VERIFY_TOKEN=seu_token_aqui
GESTORES_AUTORIZADOS=+5511999999999
```

### 3. Executar Backend

```powershell
cd backend
python run.py
```

### 4. Testar Comandos

```powershell
# Endpoint de teste (desenvolvimento)
curl -X POST "http://localhost:8000/webhook/whatsapp/test?comando=1&telefone=%2B5511999999999"
```

### 5. Configurar WhatsApp

Siga o guia: `docs/INSTALACAO_WHATSAPP.md`

---

## 📊 COMANDOS DISPONÍVEIS

### Mais Importantes:

| Comando | Descrição | Quando Usar |
|---------|-----------|-------------|
| `1` | Resumo Geral | Início do dia |
| `12` | **Empresas Paradas** | **DIARIAMENTE** (🔴 prioritário) |
| `6` | Declarações Pendentes | Acompanhar prazos |
| `4` | Sem Faturamento | Dispensar obrigações |
| `8` | Tempo de Finalização | Análise de eficiência |

### Rotina Diária Recomendada:

```
08:00 → Digite: 1  (Resumo Geral)
08:05 → Digite: 12 (Empresas Paradas) ⚠️ PRIORITÁRIO
08:10 → Digite: 6  (Declarações Pendentes)

Durante o dia → Busque empresas por nome
17:00 → Digite: 1  (Ver progresso do dia)
```

**Ver lista completa:** `docs/COMANDOS_WHATSAPP.md`

---

## 📈 MÉTRICAS E ANÁLISES

### Dados Disponíveis:

✅ **211 Empresas**
- 5 regimes tributários
- Competência: 10/2025
- Status: concluídos, em andamento, parados

✅ **Análises Gerenciais**
- Taxa de conclusão por regime
- Tempo médio de processamento
- Empresas sem faturamento
- Tributos apurados
- Declarações pendentes/dispensadas
- Gargalos identificados

✅ **Alertas Inteligentes**
- Empresas paradas (0% progresso)
- Processos críticos/atrasados
- Desdobramentos não respondidos
- Prazos próximos do vencimento

✅ **Busca e Filtros**
- Buscar por nome da empresa
- Buscar por CNPJ
- Filtrar por status

---

## 🛠️ TECNOLOGIAS

### Backend:
- **Python 3.10+**
- **FastAPI** - API REST
- **SQLAlchemy** - ORM
- **SQLite** - Banco de dados
- **Pydantic** - Validação

### WhatsApp:
- **Meta Cloud API** (gratuito)
- ou **Evolution API** (gratuito, self-hosted)

### Infraestrutura:
- **Ngrok** - Exposição local (desenvolvimento)
- **Heroku/AWS** - Produção (opcional)

---

## 📚 DOCUMENTAÇÃO

### Guias Principais:

1. **GESTOR_WHATSAPP_ESPECIFICACAO.md**
   - Visão completa do sistema
   - Arquitetura detalhada
   - Exemplos de relatórios
   - 📍 `docs/GESTOR_WHATSAPP_ESPECIFICACAO.md`

2. **INSTALACAO_WHATSAPP.md**
   - Passo a passo de instalação
   - Configuração do WhatsApp
   - Meta Cloud API vs Evolution API
   - Solução de problemas
   - 📍 `docs/INSTALACAO_WHATSAPP.md`

3. **COMANDOS_WHATSAPP.md**
   - Lista completa de comandos
   - Exemplos práticos
   - Rotinas recomendadas
   - Dicas de uso
   - 📍 `docs/COMANDOS_WHATSAPP.md`

4. **backend/whatsapp/README.md**
   - Documentação técnica
   - API do módulo
   - Como adicionar novos comandos
   - 📍 `backend/whatsapp/README.md`

---

## 🔧 MÓDULOS CRIADOS

### 1. backend/whatsapp/analytics.py
**Classe:** `GestorAnalytics`

Responsável por todas as análises e cálculos de KPIs:
- Resumo geral
- Análise por regime
- Empresas sem faturamento
- Empresas com tributos
- Declarações pendentes
- Tempo de finalização
- Empresas paradas
- Gargalos
- Desdobramentos pendentes
- Busca de empresas

### 2. backend/whatsapp/formatador.py
**Classe:** `WhatsAppFormatter`

Formatação de relatórios para WhatsApp:
- Templates otimizados para mobile
- Emojis e símbolos
- Barras de progresso ASCII
- Tabelas formatadas
- Box com títulos

### 3. backend/whatsapp/processor.py
**Classe:** `CommandProcessor`

Processamento de comandos:
- Interpreta 24 comandos diferentes
- Gerencia estado da conversação
- Roteia para análise correta
- Gera resposta formatada

### 4. backend/whatsapp/webhook.py
**Router FastAPI:** `/webhook/whatsapp`

Integração com WhatsApp Business API:
- Recebe mensagens via webhook
- Valida gestores autorizados
- Processa comandos
- Envia respostas
- Logs de auditoria

---

## 💡 EXEMPLOS DE USO

### Exemplo 1: Desbloquear Processos

```
👤 Gestor: 12
🤖 Bot: 🛑 35 empresas paradas
        Motivo: Aguardando Faturamento (28)

[Gestor coleta informações das empresas]

👤 Gestor: 12
🤖 Bot: 🛑 7 empresas paradas
        ✅ 28 empresas desbloqueadas!
```

### Exemplo 2: Evitar Multa

```
👤 Gestor: 6
🤖 Bot: 🔴 DAS - Prazo: 2 dias
        Pendentes: 144 empresas ⚠️

[Gestor prioriza entrega do DAS]

👤 Gestor: 6
🤖 Bot: 🟢 DAS - Prazo: HOJE
        Pendentes: 5 empresas
        ✅ 139 entregues!
```

### Exemplo 3: Buscar Empresa

```
👤 Gestor: MOUSSA
🤖 Bot: 🏢 MOUSSA CONSTRUTORA LTDA
        CNPJ: 38.135.574/0001-40
        Status: Em andamento (0%)
        Bloqueio: Aguardando Faturamento
        Ação: Contatar empresa
```

---

## 🔒 SEGURANÇA

✅ **Autenticação**
- Apenas números autorizados podem usar
- Configurado em `.env` → `GESTORES_AUTORIZADOS`

✅ **Validação de Assinatura**
- Webhook valida assinatura HMAC (Meta API)
- Previne falsificação de mensagens

✅ **HTTPS Obrigatório**
- Webhook deve usar HTTPS
- Dados criptografados em trânsito

✅ **Logs de Auditoria**
- Todos os comandos são registrados
- Timestamp, telefone, comando

---

## 💰 CUSTOS

### Opção 1: Meta Cloud API (Recomendado)
- ✅ 1.000 conversas gratuitas/mês
- ✅ Oficial do Meta/Facebook
- ✅ Confiável e escalável
- 💰 Após 1.000: $0.005-$0.09 por conversa

### Opção 2: Evolution API (Gratuito)
- ✅ 100% Gratuito
- ✅ Sem limites
- ✅ Open source
- ⚠️ Requer servidor próprio

### Recomendação:
Para este uso (apenas recebe comandos do gestor), **ambas opções são 100% gratuitas** pois:
1. Meta Cloud API: <1.000 conversas/mês
2. Evolution API: Self-hosted gratuito

---

## 🐛 SOLUÇÃO DE PROBLEMAS

### Problema: "Comando não reconhecido"
**Solução:** Digite `0` para ver o menu

### Problema: "Telefone não autorizado"
**Solução:** Adicione seu número em `.env` → `GESTORES_AUTORIZADOS`

### Problema: "Webhook não recebe mensagens"
**Solução:** 
1. Verifique se backend está rodando
2. Verifique ngrok/URL pública
3. Confirme configuração no Meta/Evolution API

### Problema: "Dados desatualizados"
**Solução:** 
```powershell
cd backend
python -m app.services.acessorias_sync
```

---

## 🚀 PRÓXIMOS PASSOS

### Fase 1: Configurar (1-2 horas) ✅
1. ✅ Criar `.env`
2. ✅ Executar backend
3. ✅ Configurar WhatsApp
4. ✅ Testar comandos

### Fase 2: Usar Diariamente (1 semana)
1. Familiarizar com comandos principais (1, 12, 6)
2. Criar rotina diária
3. Identificar comandos mais úteis

### Fase 3: Otimizar (2 semanas)
1. Personalizar comandos
2. Adicionar análises específicas
3. Ajustar formatação de relatórios

### Fase 4: Expandir (1 mês)
1. Adicionar alertas automáticos
2. Notificações agendadas
3. Integrar com outros sistemas

---

## 📊 BENEFÍCIOS

✅ **Mobilidade**
- Acesso de qualquer lugar via WhatsApp
- Não precisa abrir notebook

✅ **Velocidade**
- Respostas em 1-3 segundos
- Decisões rápidas baseadas em dados

✅ **Insights**
- Identifica gargalos automaticamente
- Sugere ações prioritárias

✅ **Produtividade**
- 24 análises diferentes
- Elimina planilhas Excel
- Foco no que importa

✅ **Custo Zero**
- 100% gratuito
- Sem mensagens automáticas

---

## 🆘 SUPORTE

### Documentação:
- 📖 Especificação: `docs/GESTOR_WHATSAPP_ESPECIFICACAO.md`
- 📦 Instalação: `docs/INSTALACAO_WHATSAPP.md`
- 📝 Comandos: `docs/COMANDOS_WHATSAPP.md`
- 💻 Técnico: `backend/whatsapp/README.md`

### Contato:
- 📧 Email: seu_email@empresa.com
- 💬 WhatsApp: +55 11 99999-9999

---

## 📜 HISTÓRICO DE VERSÕES

### v1.0 (18/11/2025) - Primeira Versão ✅
- ✅ Módulo de análise completo (analytics.py)
- ✅ Formatação para WhatsApp (formatador.py)
- ✅ Processador de 24 comandos (processor.py)
- ✅ Webhook WhatsApp integrado (webhook.py)
- ✅ Documentação completa
- ✅ Guias de instalação e uso
- ✅ Testes unitários

### Próximas Versões:
- v1.1: Cache de consultas frequentes
- v1.2: Notificações agendadas
- v1.3: Machine Learning para previsões

---

## 📄 LICENÇA

Este projeto é de uso interno da empresa. Todos os direitos reservados.

---

## 🙏 AGRADECIMENTOS

- **FastAPI** - Framework web moderno
- **SQLAlchemy** - ORM robusto
- **Meta/Facebook** - WhatsApp Business API
- **Evolution API** - Alternativa open source

---

## 🎓 APRENDIZADOS

Este projeto demonstra:
- ✅ Integração com WhatsApp Business API
- ✅ Processamento de comandos via mensagens
- ✅ Análise de dados em tempo real
- ✅ Formatação otimizada para mobile
- ✅ Arquitetura modular e escalável
- ✅ Documentação completa

---

**Última atualização:** 18/11/2025  
**Versão:** 1.0.0  
**Status:** ✅ Pronto para Produção

---

## 🚀 COMEÇAR AGORA

```powershell
# 1. Instalar
cd "c:\acessorias processos"
pip install -r requirements.txt

# 2. Configurar
copy .env.example .env
notepad .env

# 3. Executar
cd backend
python run.py

# 4. Testar
curl http://localhost:8000/webhook/whatsapp/status

# 5. Ler documentação
start docs\INSTALACAO_WHATSAPP.md
```

**Boa gestão! 📱📊**
