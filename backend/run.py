"""
Script para iniciar o servidor Backend FastAPI
"""
import uvicorn
import sys
from pathlib import Path

# Adicionar diretório raiz ao path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print(" 🚀 BACKEND API - GESTÃO DE PROCESSOS CONTÁBEIS")
    print("=" * 70)
    print(" FastAPI + SQLAlchemy + SQLite")
    print(" URL: http://localhost:8000")
    print(" Docs: http://localhost:8000/docs")
    print(" ReDoc: http://localhost:8000/redoc")
    print("=" * 70 + "\n")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
