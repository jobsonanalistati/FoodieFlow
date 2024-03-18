from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from core.model.cliente import Cliente as ClienteModel


class ClienteRepository(ABC):
    @abstractmethod
    def create_cliente(self, db: Session, cliente: ClienteModel):
        pass

    @abstractmethod
    def get_cliente(self, db: Session, cliente_id: int):
        pass

    @abstractmethod
    def get_cliente_by_cpf(self, db: Session, cpf: str):
        pass

    @abstractmethod
    def get_cliente_by_email(self, db: Session, email: str):
        pass

    @abstractmethod
    def get_clientes(self, db: Session, skip: int = 0, limit: int = 100):
        pass

    @abstractmethod
    def update_cliente(
        self, db: Session, cliente_id: int, updated_cliente: ClienteModel
    ):
        pass

    @abstractmethod
    def delete_cliente(self, db: Session, cliente_id: int):
        pass
