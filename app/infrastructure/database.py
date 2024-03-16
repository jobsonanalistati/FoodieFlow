import os

from decouple import config
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

load_dotenv()

# Pegando as configuracoes do .env
DB_USER = config("POSTGRES_USER", default=os.getenv("POSTGRES_USER"))
DB_PASSWORD = config("POSTGRES_PASSWORD", default=os.getenv("POSTGRES_PASSWORD"))
DB_NAME = config("POSTGRES_DB", default=os.getenv("POSTGRES_DB"))
DB_HOST = config("POSTGRES_HOST", default=os.getenv("POSTGRES_HOST"))

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
)

Base = declarative_base()

engine = create_engine(SQLALCHEMY_DATABASE_URL)


def init_db():
    print(SQLALCHEMY_DATABASE_URL)
    if not database_exists(SQLALCHEMY_DATABASE_URL):
        # Create the database if it doesn't exist
        create_database(SQLALCHEMY_DATABASE_URL)
    Base.metadata.create_all(bind=engine)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
