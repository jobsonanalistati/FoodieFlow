from core.model.cliente import Cliente as ClienteModel
from core.model.orm.cliente import Cliente as ClienteORM
from core.ports.cliente_repository import ClienteRepository
from sqlalchemy.orm import Session


class ClienteDatabaseAdapter(ClienteRepository):
    def create_cliente(self, db: Session, cliente: ClienteModel):
        db_cliente = ClienteORM(**cliente.dict())
        db.add(db_cliente)
        db.commit()
        db.refresh(db_cliente)
        return db_cliente

    def get_cliente(self, db: Session, cliente_id: int):
        return db.query(ClienteORM).filter(ClienteORM.id == cliente_id).first()

    def get_cliente_by_cpf(self, db: Session, cpf: str):
        return db.query(ClienteORM).filter(ClienteORM.cpf == cpf).first()
    
    def get_cliente_by_email(self, db: Session, email: str):
        return db.query(ClienteORM).filter(ClienteORM.email == email).first()

    def get_clientes(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(ClienteORM).offset(skip).limit(limit).all()

    def update_cliente(
        self, db: Session, cliente_id: int, updated_cliente: ClienteModel
    ):
        db_cliente = db.query(ClienteORM).filter(ClienteORM.id == cliente_id).first()
        for field, value in updated_cliente.dict(exclude_unset=True).items():
            setattr(db_cliente, field, value)
        db.commit()
        db.refresh(db_cliente)
        return db_cliente

    def delete_cliente(self, db: Session, cliente_id: int):
        db_cliente = db.query(ClienteORM).filter(ClienteORM.id == cliente_id).first()
        if not db_cliente:
            return False
        db.delete(db_cliente)
        db.commit()
        return True
