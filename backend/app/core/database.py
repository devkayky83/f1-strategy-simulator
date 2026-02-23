# Configuração do banco de dados PostgreSQL com SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from app.core.config import settings

# Engine do SQLAlchemy
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_pre_ping=True,
)

# Fabricante de sessões
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base para os modelos
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    # Dependência para obter sessão do banco de dados
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

def init_db() -> None:
    # Inicializa o banco de dados criando todas as tabelas
    
    from app.models import circuit, tire_compound, strategy, simulation
    
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")


def drop_db() -> None:
    # Remove todas as tabelas do banco de dados
    
    if settings.ENVIRONMENT == "production":
        raise Exception("Não é permitido dropar banco em produção!")
    
    Base.metadata.drop_all(bind=engine)
    print("Tabelas removidas com sucesso!")
    

def check_db_connection() -> bool:
    # Verifica a conexão com o banco de dados
    
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return True
    except Exception as e: 
        print(f"Erro ao conectar ao banco de dados: {e}")
        return False
    

if __name__ == "__main__":
    if check_db_connection():
        print("Conexão com o banco de dados OK!")
    else:
        print("Falha na conexão com o banco de dados.")