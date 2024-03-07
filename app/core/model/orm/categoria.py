from infrastructure.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR
from sqlalchemy.ext.declarative import declarative_base


class Categoria(Base):
    __tablename__ = "categoria"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, nullable=False)
