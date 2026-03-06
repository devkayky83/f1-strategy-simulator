# F1 Strategy Simulator - API Principal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.database import check_db_connection
import uvicorn


# Criando aplicação FASTAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    **F1 Race Strategy Simulator API**
    
    Simule estrátegias de corrida de Fórmula 1 com física realista:
    - Degradação de pneus não-linear
    - Consumo de combustível
    - Otimização de Pit stop
    - Comparação de estratégias
    
    Desenvolvido com ❤️ e paixão por F1
    """,
    docs_url="/docs",
    redoc_url="/redoc"
)


# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
)


# Rotas de Health Check
@app.get("/", tags=["Heath"]) # Informações da API
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "message": "Welcome to F1 Strategy Simulator API!"
    }
    

@app.get("/health", tags=["Health"])
async def health_check():
    # Verifica conexão de banco de dados
    
    db_status = check_db_connection()
    
    health = {
        "status": "healthy" if db_status else "unhealthy",
        "api": "ok",
        "database": "connected" if db_status else "disconnected",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }
    
    if not db_status:
        return JSONResponse (
            status_code=503,
            content=health
        )
    
    return health



# Exemplo de rota de simulação
@app.get("/api/v1/info", tags=["Info"])
async def get_api_info():
    # Informações sobre a API e capacidades
    return {
        "simulator_version": "1.0.0",
        "features": [
            "Simulação de degradação de pneu (Não linear com cliff)",
            "Modelo de comsumo de combustível",
            "Otimização de Pit stop",
            "Comparação de estratégias",
            "Dados de circuitos reais da F1",
            "Multíplos compostos de pneus (C1-C5, INT, WET)"
        ],
        "circuitos disponíveis": 6,
        "compostos de pneus": 7,
        "velocidade de simulação": "Ajustável (1x - 100x)",
        "endpoints": {
            "circuits": "/api/v1/circuits",
            "strategies": "/api/v1/strategies",
            "simulation": "/api/v1/simulation",
            "comparison": "/api/v1/strategies/compare"
        }
    }
    

# Erros de Handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": "The requested resource was not found",
            "docs": "/docs"
        }
    )
    

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected erro occurred. Please try again later."
        }
    )
    

# Eventos de Startup e Shotdowns
@app.on_event("startup")
async def startup_event():
    print("\n" + "="*60)
    print(f"- {settings.APP_NAME} v{settings.APP_VERSION}")
    print("="*60)
    print(f"- API rodando em: http://{settings.HOST}:{settings.PORT}")
    print(f"- Documentação: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"- Environment: {settings.ENVIRONMENT}")
    print(f"- Database: {'Connected ✓' if check_db_connection() else 'Disconnected X'}")
    print("="*60 + "\n")
    

@app.on_event("shutdown")
async def shutdown_event():
    print("\n Shutting down F1 Strategy Simulator API...")
    
    

# MAIN
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )