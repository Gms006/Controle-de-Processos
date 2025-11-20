"""
Webhook WhatsApp Business API
Recebe mensagens e envia respostas
"""

from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import PlainTextResponse
from typing import Dict, Optional
import hmac
import hashlib
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis de ambiente
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)

from .processor import CommandProcessor
from .formatador import WhatsAppFormatter


# Router FastAPI
router = APIRouter(prefix="/webhook/whatsapp", tags=["WhatsApp"])

# Configurações
WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "acessorias_gestor_2025_token_secreto")
WHATSAPP_APP_SECRET = os.getenv("WHATSAPP_APP_SECRET", "")
GESTORES_AUTORIZADOS = os.getenv("GESTORES_AUTORIZADOS", "").split(",")

print(f"🔑 Verify Token carregado: {WHATSAPP_VERIFY_TOKEN[:20]}...")
print(f"👥 Gestores autorizados: {GESTORES_AUTORIZADOS}")

# Processador de comandos (singleton)
processor = CommandProcessor()


# ============ AUTENTICAÇÃO ============

def verificar_assinatura(payload: bytes, signature: str) -> bool:
    """
    Verifica assinatura HMAC do webhook (Meta/Facebook)
    """
    if not WHATSAPP_APP_SECRET:
        return True  # Desenvolvimento sem verificação
    
    expected_signature = hmac.new(
        WHATSAPP_APP_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(f"sha256={expected_signature}", signature)


def gestor_autorizado(telefone: str) -> bool:
    """
    Verifica se o número está autorizado a usar o sistema
    """
    if not GESTORES_AUTORIZADOS[0]:
        return True  # Desenvolvimento sem restrição
    
    # Normalizar telefone
    telefone_limpo = telefone.replace("+", "").replace(" ", "").replace("-", "")
    
    for gestor in GESTORES_AUTORIZADOS:
        gestor_limpo = gestor.replace("+", "").replace(" ", "").replace("-", "")
        if telefone_limpo == gestor_limpo:
            return True
    
    return False


# ============ WEBHOOK ENDPOINTS ============

@router.get("/")
async def webhook_verificacao(request: Request):
    """
    Endpoint de verificação do webhook (Meta/Facebook)
    GET com query params: hub.mode, hub.verify_token, hub.challenge
    """
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    
    if mode == "subscribe" and token == WHATSAPP_VERIFY_TOKEN:
        print(f"✅ Webhook verificado com sucesso!")
        return PlainTextResponse(challenge)
    
    raise HTTPException(status_code=403, detail="Token de verificação inválido")


@router.post("/")
async def webhook_mensagem(request: Request):
    """
    Endpoint principal do webhook
    Recebe mensagens do WhatsApp e responde
    """
    # Verificar assinatura (segurança) - APENAS EM PRODUÇÃO
    signature = request.headers.get("X-Hub-Signature-256", "")
    payload = await request.body()
    
    # Em desenvolvimento, permitir sem assinatura para testes
    if WHATSAPP_APP_SECRET and signature and not verificar_assinatura(payload, signature):
        raise HTTPException(status_code=403, detail="Assinatura inválida")
    
    # Parse JSON
    data = await request.json()
    
    # Processar mensagem
    try:
        resposta = processar_webhook(data)
        return {"status": "success", "resposta": resposta}
    
    except Exception as e:
        print(f"❌ Erro ao processar webhook: {e}")
        return {"status": "error", "message": str(e)}


# ============ PROCESSAMENTO DE MENSAGENS ============

def processar_webhook(data: Dict) -> Optional[str]:
    """
    Processa payload do webhook e retorna resposta
    """
    # Estrutura do webhook Meta/Facebook:
    # {
    #   "object": "whatsapp_business_account",
    #   "entry": [{
    #     "changes": [{
    #       "value": {
    #         "messages": [{
    #           "from": "5511999999999",
    #           "text": {"body": "mensagem"}
    #         }]
    #       }
    #     }]
    #   }]
    # }
    
    if data.get("object") != "whatsapp_business_account":
        return None
    
    entries = data.get("entry", [])
    
    for entry in entries:
        changes = entry.get("changes", [])
        
        for change in changes:
            value = change.get("value", {})
            messages = value.get("messages", [])
            
            for message in messages:
                # Extrair dados da mensagem
                telefone = message.get("from")
                texto = message.get("text", {}).get("body", "")
                
                if not telefone or not texto:
                    continue
                
                # Verificar autorização
                if not gestor_autorizado(telefone):
                    resposta = WhatsAppFormatter.erro_nao_autorizado()
                    enviar_mensagem_whatsapp(telefone, resposta)
                    continue
                
                # Processar comando
                resposta = processor.processar(texto, telefone)
                
                # Enviar resposta
                enviar_mensagem_whatsapp(telefone, resposta)
                
                # Log
                registrar_log(telefone, texto, resposta)
                
                return resposta
    
    return None


def enviar_mensagem_whatsapp(telefone: str, mensagem: str):
    """
    Envia mensagem via WhatsApp Business API
    
    NOTA: Esta é a parte que ENVIA mensagens.
    Para uso 100% gratuito, você pode:
    1. Usar apenas como RESPOSTA (dentro da janela de 24h)
    2. Usar Evolution API (gratuito, self-hosted)
    3. Comentar esta função para apenas logar
    """
    # TODO: Implementar envio real
    # Opções:
    # - Meta Cloud API (gratuito para respostas)
    # - Evolution API (gratuito, self-hosted)
    # - Twilio (pago)
    
    print(f"📤 Enviando para {telefone}:")
    print(mensagem[:200])
    print("...")
    
    # Exemplo de implementação com Meta Cloud API:
    # import requests
    # 
    # url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    # headers = {
    #     "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
    #     "Content-Type": "application/json"
    # }
    # data = {
    #     "messaging_product": "whatsapp",
    #     "to": telefone,
    #     "type": "text",
    #     "text": {"body": mensagem}
    # }
    # 
    # response = requests.post(url, headers=headers, json=data)
    # return response.json()


def registrar_log(telefone: str, comando: str, resposta: str):
    """
    Registra comando executado em log de auditoria
    """
    timestamp = datetime.now().isoformat()
    
    log_entry = {
        "timestamp": timestamp,
        "telefone": telefone,
        "comando": comando,
        "resposta_tamanho": len(resposta),
        "resposta_preview": resposta[:100]
    }
    
    print(f"📝 LOG: {log_entry}")
    
    # TODO: Salvar em arquivo ou banco de dados
    # with open("logs/whatsapp_commands.log", "a") as f:
    #     f.write(f"{timestamp} | {telefone} | {comando}\n")


# ============ ENDPOINTS AUXILIARES ============

@router.get("/status")
async def status():
    """
    Verifica status do webhook
    """
    return {
        "status": "online",
        "webhook_url": "/webhook/whatsapp",
        "gestores_cadastrados": len([g for g in GESTORES_AUTORIZADOS if g]),
        "verify_token_configurado": bool(WHATSAPP_VERIFY_TOKEN)
    }


@router.post("/test")
async def test_comando(comando: str, telefone: str = "+5511999999999"):
    """
    Endpoint de teste (apenas desenvolvimento)
    Permite testar comandos sem configurar WhatsApp
    """
    if not gestor_autorizado(telefone):
        return {
            "erro": "Telefone não autorizado",
            "telefone": telefone,
            "gestores": GESTORES_AUTORIZADOS
        }
    
    resposta = processor.processar(comando, telefone)
    
    return {
        "comando": comando,
        "telefone": telefone,
        "resposta": resposta
    }


# ============ CONFIGURAÇÃO ============

class WhatsAppWebhook:
    """
    Classe de configuração do webhook
    """
    
    @staticmethod
    def configurar_app(app):
        """
        Adiciona router ao app FastAPI
        """
        app.include_router(router)
        print("✅ Webhook WhatsApp configurado")
    
    @staticmethod
    def adicionar_gestor(telefone: str):
        """
        Adiciona número autorizado
        """
        global GESTORES_AUTORIZADOS
        if telefone not in GESTORES_AUTORIZADOS:
            GESTORES_AUTORIZADOS.append(telefone)
            print(f"✅ Gestor adicionado: {telefone}")
    
    @staticmethod
    def remover_gestor(telefone: str):
        """
        Remove número autorizado
        """
        global GESTORES_AUTORIZADOS
        if telefone in GESTORES_AUTORIZADOS:
            GESTORES_AUTORIZADOS.remove(telefone)
            print(f"❌ Gestor removido: {telefone}")


# ============ TESTE ============

if __name__ == "__main__":
    print("🔌 Testando Webhook WhatsApp...\n")
    
    # Simular mensagem recebida
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
    
    print("📩 Processando mensagem de teste...")
    resposta = processar_webhook(payload_teste)
    print(f"\n✅ Resposta gerada ({len(resposta)} caracteres)")
    print(resposta[:300], "...\n")
    
    print("✅ Webhook OK!")
