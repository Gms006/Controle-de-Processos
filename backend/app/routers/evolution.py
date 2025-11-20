"""
Router para receber webhooks da Evolution API
"""
from fastapi import APIRouter, Request, Header
from typing import Optional
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/evolution", tags=["Evolution API"])

@router.post("/webhook")
async def evolution_webhook(request: Request, apikey: Optional[str] = Header(None)):
    """Recebe webhooks da Evolution API incluindo QR Code"""
    try:
        body = await request.json()
        event = body.get("event")
        
        logger.info(f"📥 Evolution Webhook: {event}")
        
        if event == "qrcode.updated":
            qr_data = body.get("data", {})
            qr_code = qr_data.get("qrcode", {}).get("code")
            qr_base64 = qr_data.get("qrcode", {}).get("base64")
            
            if qr_base64:
                logger.info("=" * 80)
                logger.info("🔲 QR CODE GERADO!")
                logger.info("=" * 80)
                logger.info(f"Base64: {qr_base64[:100]}...")
                logger.info("=" * 80)
                logger.info("💡 Salve este base64 ou acesse:")
                logger.info("   data:image/png;base64," + qr_base64)
                logger.info("=" * 80)
                
                # Salvar em arquivo para fácil acesso
                import base64
                with open("qrcode_evolution.txt", "w") as f:
                    f.write(f"data:image/png;base64,{qr_base64}")
                logger.info("✅ QR Code salvo em qrcode_evolution.txt")
        
        elif event == "connection.update":
            conn_data = body.get("data", {})
            state = conn_data.get("state")
            logger.info(f"🔌 Conexão atualizada: {state}")
        
        elif event == "messages.upsert":
            logger.info("📨 Nova mensagem recebida!")
        
        return {"status": "success", "event": event}
        
    except Exception as e:
        logger.error(f"❌ Erro no webhook Evolution: {e}")
        return {"status": "error", "message": str(e)}

@router.get("/qrcode")
async def get_qrcode():
    """Retorna o último QR Code salvo"""
    try:
        with open("qrcode_evolution.txt", "r") as f:
            qr_data = f.read()
        return {"status": "success", "qrcode": qr_data}
    except FileNotFoundError:
        return {"status": "error", "message": "QR Code não gerado ainda"}
