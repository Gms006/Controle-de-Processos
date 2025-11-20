"""
WhatsApp Router - Integração com webhook
"""
from fastapi import APIRouter, Request, HTTPException, Header
from typing import Optional
import os
import hmac
import hashlib
from pathlib import Path
import sys

# Adicionar diretório backend ao path ANTES de importar
backend_dir = Path(__file__).parent.parent.parent
whatsapp_path = backend_dir / "whatsapp"

if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# Agora importar o router
try:
    from whatsapp.webhook import router
    print(f"✅ WhatsApp webhook importado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao importar webhook: {e}")
    print(f"   Backend dir: {backend_dir}")
    print(f"   WhatsApp path: {whatsapp_path}")
    print(f"   Existe? {whatsapp_path.exists()}")
    # Criar router vazio caso falhe
    router = APIRouter()

__all__ = ['router']
