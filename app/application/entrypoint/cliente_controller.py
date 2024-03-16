import daiquiri
import boto3
import os
from core.model.cliente import Cliente as ClienteModel
from core.ports.cliente_repository import ClienteRepository
from core.usecases.cliente_service_impl import ClienteServiceImpl
from fastapi import APIRouter, Depends, HTTPException
from infrastructure.database import get_db
from infrastructure.dataprovider.cliente_database_adapter import ClienteDatabaseAdapter
from sqlalchemy.orm import Session

router = APIRouter()
log = daiquiri.getLogger(__name__)

cliente_repository: ClienteRepository = ClienteDatabaseAdapter()
cliente_service = ClienteServiceImpl(cliente_repository)
COGNITO_REGION = os.getenv("COGNITO_REGION")
CLIENT_ID = os.getenv("CLIENT_ID")
client = boto3.client("cognito-idp", region_name=COGNITO_REGION)


@router.post("/", response_model=ClienteModel, description="Cria um novo cliente")
def create_cliente(cliente: ClienteModel, db: Session = Depends(get_db)):
    try:
        log.info(f"Cliente para criação: {cliente}")
        try:
            log.info("Iniciando a criação do usuário no cognito")
            client.sign_up(
                ClientId=CLIENT_ID,
                Username=format_cpf(cliente.cpf) if cliente.cpf else cliente.email,
                Password="Foodieflow@123",
                UserAttributes=[
                    {"Name": "name", "Value": cliente.nome},
                    {"Name": "email", "Value": cliente.email},
                ],
            )
            log.info("Usuário no cognito criado com sucesso!")
        except client.exceptions.UsernameExistsException:
            raise HTTPException(status_code=400, detail="Username já existe!")

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        return cliente_service.create_cliente(db, cliente)
    except Exception as ex:
        log.error(f"Erro ao criar cliente. {str(ex)}")

        if "Cliente já cadastrado" in str(ex):
            raise HTTPException(status_code=400, detail="Cliente já cadastrado")

        raise HTTPException(status_code=400, detail="Erro ao criar cliente")


@router.get(
    "/{cliente_id}", response_model=ClienteModel, description="Busca um cliente pelo ID"
)
def read_cliente(cliente_id: int, db: Session = Depends(get_db)):
    try:
        log.info(f"Buscando cliente com ID {cliente_id}")
        cliente = cliente_service.get_cliente(db, cliente_id)
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        return cliente
    except HTTPException:
        raise
    except Exception as ex:
        log.error(f"Erro ao buscar cliente. {str(ex)}")
        raise HTTPException(status_code=400, detail="Erro ao buscar cliente")


@router.get(
    "/bycpf/{cpf}", response_model=ClienteModel, description="Busca um cliente pelo CPF"
)
def read_cliente_by_cpf(cpf: str, db: Session = Depends(get_db)):
    try:
        log.info(f"Buscando cliente com CPF {cpf}")
        cliente = cliente_service.get_cliente_by_cpf(db, cpf)
        if not cliente:
            raise HTTPException(
                status_code=404, detail="Cliente não encontrado pelo CPF"
            )
        return cliente
    except HTTPException:
        raise
    except Exception as ex:
        log.error(f"Erro ao buscar cliente pelo CPF. {str(ex)}")
        raise HTTPException(status_code=400, detail="Erro ao buscar cliente pelo CPF")


@router.get(
    "/bycpf/{email}",
    response_model=ClienteModel,
    description="Busca um cliente pelo EMAIL",
)
def read_cliente_by_email(email: str, db: Session = Depends(get_db)):
    try:
        log.info(f"Buscando cliente com email {email}")
        cliente = cliente_service.get_cliente_by_email(db, email)
        if not cliente:
            raise HTTPException(
                status_code=404, detail="Cliente não encontrado pelo email"
            )
        return cliente
    except HTTPException:
        raise
    except Exception as ex:
        log.error(f"Erro ao buscar cliente pelo email. {str(ex)}")
        raise HTTPException(status_code=400, detail="Erro ao buscar cliente pelo email")


@router.get(
    "/", response_model=list[ClienteModel], description="Busca todos os clientes"
)
def read_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        log.info("Buscando clientes")
        return cliente_service.get_clientes(db, skip, limit)
    except Exception as ex:
        log.error(f"Erro ao buscar clientes. {str(ex)}")
        raise HTTPException(status_code=400, detail="Erro ao buscar clientes")


@router.put(
    "/{cliente_id}", response_model=ClienteModel, description="Atualiza um cliente"
)
def update_cliente(
    cliente_id: int, updated_cliente: ClienteModel, db: Session = Depends(get_db)
):
    try:
        log.info(f"Cliente recebido para atualização: {updated_cliente}")
        cliente = cliente_service.update_cliente(db, cliente_id, updated_cliente)
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        return cliente
    except HTTPException:
        raise
    except Exception as ex:
        log.error(f"Erro ao atualizar cliente. {str(ex)}")
        raise HTTPException(status_code=400, detail="Erro ao atualizar cliente")


@router.delete("/{cliente_id}", description="Deleta um cliente")
def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    try:
        log.info(f"Deletando cliente com ID {cliente_id}")
        success = cliente_service.delete_cliente(db, cliente_id)
        if not success:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        return {"message": "Cliente deletado com sucesso!"}
    except HTTPException:
        raise
    except Exception as ex:
        log.error(f"Erro ao deletar cliente: {str(ex)}")
        raise HTTPException(status_code=400, detail="Erro ao deletar cliente")


def format_cpf(cpf):
    cpf = "".join(filter(str.isdigit, cpf))

    formatted_cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

    return formatted_cpf
