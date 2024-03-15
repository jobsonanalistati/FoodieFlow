from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER
from sqlalchemy.ext.declarative import declarative_base

from infrastructure.database import Base


class Status(Base):
    __tablename__ = "status"

    id = Column(INTEGER, primary_key=True, index=True, autoincrement=True)
    nome = Column(VARCHAR(25), unique=True, index=True, nullable=False)
