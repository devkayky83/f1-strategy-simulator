# Configuração central da aplicação

from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path

class Settings(BaseSettings):
    # Configurações carregadas do .env
    
    # Aplicação
    APP_NAME: str = "F1 Strategy Simulator"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Servidor
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    
    # Database
    DATABASE_URL: str
    DB_ECHO: bool = False
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    
    # Segurança
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    ALLOWED_METHODS: List[str] = ["*"]
    ALLOWED_HEADERS: List[str] = ["*"]
    
    # APIs Externas
    ERGAST_API_URL: str = "http://ergast.com/api/f1"
    OPENF1_API_URL: str = "https://api.openf1.org/v1"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_ENABLED: bool = False
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
    
    # Limite de requisições
    RATE_LIMIT_ENABLED: bool = False
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Simulação
    DEFAULT_SIMULATION_SPEED: float = 1.0
    MAX_CONCURRENT_SIMULATIONS: int = 10
    SIMULATION_TIMEOUT_SECONDS: int = 300
    
    # Caminhos
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        


# Instância global das configurações
settings = Settings()

class SimulationConstants:
    # Constantes relacionadas à simulação
    
    TIRE_DEGRADATION = {
        "C1": 0.015,
        "C2": 0.022,
        "C3": 0.030,
        "C4": 0.040,
        "C5": 0.055,
        "INTERMEDIATE": 0.025,
        "WET": 0.020,
    }
    
    TIRE_OPTIMAL_LIFE = { # Por voltas
        "C1": 40,
        "C2": 35,
        "C3": 30,
        "C4": 25,
        "C5": 20,
        "INTERMEDIATE": 30,
        "WET": 25,
    }
    
    TIRE_GRIP = {
        "C1": 0.92,
        "C2": 0.95,
        "C3": 1.00,
        "C4": 1.05,
        "C5": 1.10,
        "INTERMEDIATE": 0.85,
        "WET": 0.75,
    }
    
    # Combustível
    FUEL_EFFECT_PER_KG: float = 0.03
    FUEL_COMSUMPTION_PER_LAP: float = 1.6
    INITIAL_FUEL_LOAD: float = 110.0
    
    # Pit Stop
    PIT_STOP_TIME_MIN: float = 2.0
    PIT_STOP_TIME_MAX: float = 3.5
    PIT_LOSS_BASE: float = 20.0
    
    # Variação aleatória
    LAP_TIME_VARIATION: float = 0.2
    
    # Fatores climáticos
    TEMP_OPTIMAL: float = 25.0
    TEMP_IMPACT_FACTOR: float = 0.002
    
    # Safety Car / Virtual Safety Car
    SAFETY_CAR_PROBABILITY: float = 0.15
    VSC_PROBABILITY: float = 0.25
    
    # DRS
    DRS_ADVANTAGE: float = 0.3
    
    
    
TIRE_COLORS = {
    "C1": "FFFFFF",
    "C2": "FFFF00",
    "C3": "FFFF00",
    "C4": "FF0000",
    "C5": "FF0000",
    "INTERMEDIATE": "00FF00",
    "WET": "0000FF",
}

def validate_settings() -> bool:
    # Valida se todas as configurações essenciais estão presentes
    
    required_fields = ["DATABASE_URL", "SECRET_KEY"]
    missing = []
    
    for var in required_fields:
        if not getattr(settings, var, None):
            missing.append(var)
            
    if missing:
        raise ValueError(f"Variáveis de ambiente obrigatórias não encontradas: {', '.join(missing)}")
    
    return True


if __name__ == "__main__":
    try:
        validate_settings()
        print("Configurações validadas com sucesso!")
        print(f"App: {settings.APP_NAME} v{settings.APP_VERSION}")
        print(f"Database: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'N/A'}")
        print(f"Environment: {settings.ENVIRONMENT}")
    except ValueError as e:
        print(f"Erro nas configurações: {e}")