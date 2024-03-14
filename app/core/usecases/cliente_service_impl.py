from sqlalchemy.orm import Session
from core.ports.cliente_repository import ClienteRepository
from core.model.cliente import Cliente as ClienteModel


class ClienteServiceImpl:
    def __init__(self, cliente_repository: ClienteRepository):
        self.cliente_repository = cliente_repository

    def create_cliente(self, db: Session, cliente: ClienteModel):
        cliente_db = self.cliente_repository.get_cliente_by_cpf(db, cliente.cpf)
        if cliente_db:
            raise Exception("Cliente já cadastrado")
        return self.cliente_repository.create_cliente(db, cliente)

    def get_cliente(self, db: Session, cliente_id: int):
        return self.cliente_repository.get_cliente(db, cliente_id)

    def get_cliente_by_cpf(self, db: Session, cpf: str):
        return self.cliente_repository.get_cliente_by_cpf(db, cpf)
    
    def get_cliente_by_email(self, db: Session, email: str):
        return self.cliente_repository.get_cliente_by_email(db, email)

    def get_clientes(self, db: Session, skip: int = 0, limit: int = 100):
        return self.cliente_repository.get_clientes(db, skip, limit)

    def update_cliente(
        self, db: Session, cliente_id: int, updated_cliente: ClienteModel
    ):
        return self.cliente_repository.update_cliente(db, cliente_id, updated_cliente)

    def delete_cliente(self, db: Session, cliente_id: int):
        return self.cliente_repository.delete_cliente(db, cliente_id)
