from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# URL do banco de dados
DATABASE_URL = "mysql+pymysql://admin:password@db/filmes"

# Se estiver em testes, usar banco em memória
if os.getenv("TEST_MODE"):
    DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependência do banco para ser injetada nos endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
