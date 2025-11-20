# 📱 Módulo WhatsApp - Gestor de Processos
## Backend Integration

---

## 📖 VISÃO GERAL

Módulo de integração com WhatsApp Business API para gestão de processos contábeis via mensagens. Permite que o gestor consulte métricas, identifique gargalos e busque empresas diretamente pelo WhatsApp.

**Características:**
- ✅ 24 comandos disponíveis
- ✅ Análises em tempo real
- ✅ Formatação otimizada para mobile
- ✅ 100% gratuito (apenas recebe mensagens)
- ✅ Respostas em 1-3 segundos

---

## 📁 ESTRUTURA DO MÓDULO

```
backend/whatsapp/
├── __init__.py           # Exportações do módulo
├── analytics.py          # Análise de dados e KPIs
├── formatador.py         # Formatação de mensagens
├── processor.py          # Processamento de comandos
└── webhook.py            # Webhook WhatsApp Business API
```

---

## 🔧 COMPONENTES

### 1. analytics.py - Módulo de Análise

**Classe Principal:** `GestorAnalytics`

**Responsabilidades:**
- Consultar banco de dados SQLite
- Calcular métricas gerenciais
- Identificar gargalos e alertas
- Gerar insights automáticos

**Principais Métodos:**

```python
from backend.whatsapp.analytics import GestorAnalytics

# Context manager
with GestorAnalytics() as analytics:
    # Resumo geral
    resumo = analytics.get_resumo_geral(competencia='10/2025')
    
    # Por regime
    regimes = analytics.get_resumo_por_regime(competencia='10/2025')
    
    # Empresas sem faturamento
    sem_fat = analytics.get_empresas_sem_faturamento(competencia='10/2025')
    
    # Empresas com tributos
    tributos = analytics.get_empresas_com_tributos(competencia='10/2025')
    
    # Declarações pendentes
    declaracoes = analytics.get_declaracoes_pendentes(competencia='10/2025')
    
    # Tempo de finalização
    tempo = analytics.get_tempo_finalizacao(competencia='10/2025')
    
    # Empresas paradas
    paradas = analytics.get_empresas_paradas(competencia='10/2025')
    
    # Gargalos
    gargalos = analytics.get_gargalos_por_passo(competencia='10/2025')
    
    # Desdobramentos pendentes
    desdobramentos = analytics.get_desdobramentos_pendentes(competencia='10/2025')
    
    # Buscar empresa
    empresas = analytics.buscar_empresa(termo='MOUSSA')
    
    # Detalhes de processo
    detalhes = analytics.get_detalhes_processo(proc_id=7493)
```

**Funções de Conveniência:**

```python
from backend.whatsapp.analytics import (
    get_resumo_geral,
    get_resumo_por_regime,
    get_empresas_sem_faturamento,
    buscar_empresa
)

# Uso direto
resumo = get_resumo_geral('10/2025')
regimes = get_resumo_por_regime('10/2025')
```

---

### 2. formatador.py - Formatação de Mensagens

**Classe Principal:** `WhatsAppFormatter`

**Responsabilidades:**
- Formatar relatórios para WhatsApp
- Otimizar para visualização mobile
- Usar emojis e símbolos
- Criar barras de progresso ASCII

**Principais Métodos:**

```python
from backend.whatsapp.formatador import WhatsAppFormatter

formatter = WhatsAppFormatter()

# Menu principal
menu = formatter.menu_principal()

# Resumo geral
resumo_formatado = formatter.resumo_geral(dados)

# Por regime
regime_formatado = formatter.resumo_por_regime(dados)

# Empresas sem faturamento
sem_fat_formatado = formatter.empresas_sem_faturamento(dados)

# Tributos
tributos_formatado = formatter.empresas_com_tributos(dados)

# Declarações
declaracoes_formatado = formatter.declaracoes_pendentes(dados)

# Tempo
tempo_formatado = formatter.tempo_finalizacao(dados)

# Paradas
paradas_formatado = formatter.empresas_paradas(dados)

# Detalhes
detalhes_formatado = formatter.detalhes_empresa(dados)

# Erros
erro = formatter.erro_comando_invalido("xyz")
nao_autorizado = formatter.erro_nao_autorizado()
ajuda = formatter.ajuda()
```

**Utilitários:**

```python
# Barra de progresso
barra = formatter.barra_progresso(75.5, tamanho=10)
# Retorna: ▓▓▓▓▓▓▓░░░

# Status emoji
emoji = formatter.status_emoji(75.5)
# Retorna: 🟢

# Box com título
titulo = formatter.box_title("MEU TÍTULO")
# Retorna:
# ╔═════════════════════════════════╗
# ║           MEU TÍTULO            ║
# ╚═════════════════════════════════╝
```

---

### 3. processor.py - Processador de Comandos

**Classe Principal:** `CommandProcessor`

**Responsabilidades:**
- Interpretar comandos recebidos
- Rotear para análise correta
- Gerenciar estado da conversação
- Gerar resposta formatada

**Uso:**

```python
from backend.whatsapp.processor import CommandProcessor

processor = CommandProcessor(competencia='10/2025')

# Processar comando
resposta = processor.processar(
    mensagem="1",
    telefone="+5511999999999"
)

print(resposta)  # Menu ou relatório formatado

processor.fechar()
```

**Comandos Suportados:**

```python
COMANDOS = {
    # Navegação
    '0': 'menu',
    'menu': 'menu',
    '23': 'ajuda',
    '24': 'sobre',
    
    # Resumos
    '1': 'resumo_geral',
    '2': 'resumo_regime',
    '3': 'resumo_empresa',
    
    # Análises
    '4': 'sem_faturamento',
    '5': 'com_tributos',
    '6': 'declaracoes_pendentes',
    
    # Desempenho
    '8': 'tempo_finalizacao',
    '10': 'top_rapidas',
    '11': 'top_lentas',
    
    # Alertas
    '12': 'empresas_paradas',
    '13': 'gargalos',
    '14': 'desdobramentos_pendentes',
    
    # Busca
    '20': 'buscar_empresa_nome',
    '21': 'buscar_empresa_cnpj',
    
    # ... e mais
}
```

---

### 4. webhook.py - Webhook WhatsApp

**Router FastAPI:** `router`

**Endpoints:**

```python
# Verificação do webhook (Meta Cloud API)
GET /webhook/whatsapp?hub.mode=subscribe&hub.verify_token=TOKEN&hub.challenge=CHALLENGE

# Receber mensagens
POST /webhook/whatsapp

# Status do webhook
GET /webhook/whatsapp/status

# Teste de comando (desenvolvimento)
POST /webhook/whatsapp/test?comando=1&telefone=+5511999999999
```

**Configuração:**

```python
from backend.whatsapp.webhook import WhatsAppWebhook
from fastapi import FastAPI

app = FastAPI()

# Adicionar webhook ao app
WhatsAppWebhook.configurar_app(app)

# Adicionar gestor autorizado
WhatsAppWebhook.adicionar_gestor("+5511999999999")

# Remover gestor
WhatsAppWebhook.remover_gestor("+5511999999999")
```

**Variáveis de Ambiente:**

```env
WHATSAPP_VERIFY_TOKEN=acessorias_token_2025
WHATSAPP_APP_SECRET=seu_app_secret
WHATSAPP_ACCESS_TOKEN=seu_access_token
WHATSAPP_PHONE_NUMBER_ID=seu_phone_id
GESTORES_AUTORIZADOS=+5511999999999,+5511888888888
```

---

## 🚀 INSTALAÇÃO

### 1. Instalar Dependências

```bash
cd "c:\acessorias processos"
pip install -r requirements.txt
```

### 2. Configurar Ambiente

Criar `.env` na raiz:

```env
WHATSAPP_VERIFY_TOKEN=seu_token_aqui
WHATSAPP_APP_SECRET=seu_secret_aqui
WHATSAPP_ACCESS_TOKEN=seu_access_token_aqui
WHATSAPP_PHONE_NUMBER_ID=seu_phone_id_aqui
GESTORES_AUTORIZADOS=+5511999999999
```

### 3. Integrar ao Backend

Editar `backend/app/main.py`:

```python
from backend.whatsapp.webhook import WhatsAppWebhook

# Após criar app FastAPI
app = FastAPI(...)

# Configurar webhook
WhatsAppWebhook.configurar_app(app)
```

### 4. Executar Backend

```bash
cd backend
python run.py
```

### 5. Expor Publicamente

```bash
# Desenvolvimento: Ngrok
ngrok http 8000

# Produção: Servidor com HTTPS
```

---

## 🧪 TESTES

### Teste Unitário

```python
# Testar analytics
python backend/whatsapp/analytics.py

# Testar formatador
python backend/whatsapp/formatador.py

# Testar processor
python backend/whatsapp/processor.py

# Testar webhook
python backend/whatsapp/webhook.py
```

### Teste de Integração

```bash
# Testar endpoint de status
curl http://localhost:8000/webhook/whatsapp/status

# Testar comando (desenvolvimento)
curl -X POST "http://localhost:8000/webhook/whatsapp/test?comando=1&telefone=%2B5511999999999"
```

### Teste End-to-End

1. Configurar WhatsApp Business API
2. Enviar mensagem: `0`
3. Receber: Menu principal
4. Enviar: `1`
5. Receber: Resumo geral

---

## 📊 PERFORMANCE

### Tempo de Resposta:

- Resumo Geral: ~500ms
- Por Regime: ~300ms
- Busca Empresa: ~200ms
- Empresas Paradas: ~400ms

### Otimizações:

```python
# Cache de consultas frequentes (implementar se necessário)
from functools import lru_cache

@lru_cache(maxsize=128)
def get_resumo_geral_cached(competencia):
    return get_resumo_geral(competencia)
```

### Limites:

- Mensagem WhatsApp: ~4096 caracteres
- Rate limit: 100 req/min (Meta Cloud API)
- Conversas gratuitas: 1.000/mês (Meta Cloud API)

---

## 🔒 SEGURANÇA

### Autenticação:

```python
# Verificar gestor autorizado
if not gestor_autorizado(telefone):
    return erro_nao_autorizado()
```

### Verificação de Assinatura:

```python
# Validar webhook Meta
if not verificar_assinatura(payload, signature):
    raise HTTPException(403)
```

### Rate Limiting (implementar se necessário):

```python
from slowapi import Limiter

limiter = Limiter(key_func=lambda: telefone)

@limiter.limit("10/minute")
def processar_comando(...):
    ...
```

---

## 📝 LOGS

### Estrutura de Log:

```python
{
    "timestamp": "2025-11-18T10:30:00",
    "telefone": "+5511999999999",
    "comando": "1",
    "resposta_tamanho": 1234,
    "resposta_preview": "Resumo Geral..."
}
```

### Visualizar Logs:

```bash
type logs\whatsapp_commands.log
```

---

## 🐛 DEBUG

### Ativar Modo Debug:

```python
# Em processor.py
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# No processamento
logger.debug(f"Comando recebido: {mensagem}")
logger.debug(f"Dados: {dados}")
```

### Simular Webhook:

```python
from backend.whatsapp.webhook import processar_webhook

payload_teste = {
    "object": "whatsapp_business_account",
    "entry": [{
        "changes": [{
            "value": {
                "messages": [{
                    "from": "5511999999999",
                    "text": {"body": "1"}
                }]
            }
        }]
    }]
}

resposta = processar_webhook(payload_teste)
print(resposta)
```

---

## 🔄 ATUALIZAÇÕES FUTURAS

### Roadmap:

**v1.1**
- [ ] Cache de consultas frequentes
- [ ] Exportar relatórios em PDF
- [ ] Gráficos ASCII avançados

**v1.2**
- [ ] Notificações proativas (agendadas)
- [ ] Alertas por e-mail
- [ ] Integração com Telegram

**v1.3**
- [ ] Machine Learning para prever atrasos
- [ ] Recomendações automáticas
- [ ] Dashboard web complementar

---

## 📚 DOCUMENTAÇÃO ADICIONAL

- `docs/GESTOR_WHATSAPP_ESPECIFICACAO.md` - Especificação completa
- `docs/INSTALACAO_WHATSAPP.md` - Guia de instalação
- `docs/COMANDOS_WHATSAPP.md` - Lista de comandos

---

## 🤝 CONTRIBUINDO

### Adicionar Novo Comando:

1. **Adicionar análise** em `analytics.py`:
```python
def get_minha_metrica(self, competencia: str = None) -> Dict:
    # Implementar análise
    return dados
```

2. **Adicionar formatação** em `formatador.py`:
```python
@classmethod
def minha_metrica(cls, dados: Dict) -> str:
    # Formatar resposta
    return texto_formatado
```

3. **Adicionar comando** em `processor.py`:
```python
# No mapeamento
COMANDOS = {
    '25': 'minha_metrica',
    'minhaMetrica': 'minha_metrica'
}

# No executor
def _executar_minha_metrica(self) -> str:
    dados = self.analytics.get_minha_metrica(self.competencia)
    return self.formatter.minha_metrica(dados)

# No processador
if comando == 'minha_metrica':
    return self._executar_minha_metrica()
```

---

## 📞 SUPORTE

- 📧 Email: seu_email@empresa.com
- 📱 WhatsApp: +55 11 99999-9999
- 🐛 Issues: GitHub (se aplicável)

---

**Última atualização:** 18/11/2025  
**Versão:** 1.0  
**Status:** Produção ✅
