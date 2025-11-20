"""
Configurações do Backend
"""
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # API
    APP_NAME: str = "Acessórias Processos API"
    APP_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # Banco de Dados SQLite
    DATABASE_URL: str = "sqlite:///./database.db"
    
    # Acessórias API
    ACESSORIAS_API_URL: str = "https://api.acessorias.com"
    ACESSORIAS_API_TOKEN: str = "7f8129c6ac10075cb95cc08c81a6f219"
    
    # Sincronização
    SYNC_BATCH_SIZE: int = 5  # Processos buscados em paralelo
    SYNC_RATE_LIMIT: float = 1.0  # Segundos entre batches
    
    # Cache
    CACHE_DIR: Path = Path("./cache")
    CACHE_TTL: int = 900  # 15 minutos
    
    # Competência padrão
    DEFAULT_COMPETENCIA: str = "10/2025"
    
    class Config:
        extra = "ignore"
        env_file = ".env"
        case_sensitive = True

settings = Settings()
