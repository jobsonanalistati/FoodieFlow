import os

from decouple import config
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

from application.commons.secret_manager import aws_connection, return_variables


client = aws_connection()
db_variables = return_variables(client)

# Pegando as configuracoes do .env
DB_USER = db_variables.get("username")
DB_PASSWORD = db_variables.get("password")
DB_NAME = db_variables.get("db_name")
DB_HOST = db_variables.get("host")


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
