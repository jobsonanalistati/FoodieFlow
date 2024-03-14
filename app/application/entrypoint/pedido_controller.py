import daiquiri
from application.commons.enums.status import StatusEnum
from core.model.pedido import Pedido as PedidoModel
from core.ports.pedido_repository import PedidoRepository
from core.usecases.pedido_service_impl import PedidoServiceImpl
from fastapi import APIRouter, Depends, HTTPException
from infrastructure.database import get_db
from infrastructure.dataprovider.pedido_database_adapter import PedidoDatabaseAdapter
from sqlalchemy.orm import Session
from application.entrypoint.cognito_controller import generate_token

router = APIRouter()
log = daiquiri.getLogger(__name__)

pedido_repository: PedidoRepository = PedidoDatabaseAdapter()
pedido_service = PedidoServiceImpl(pedido_repository)


@router.post("/", response_model=PedidoModel, description="Cria um novo pedido")
def create_pedido(pedido: PedidoModel, username: str, db: Session = Depends(get_db)):
    print("username: " + username)
    if generate_token(username):
        try:
            log.info(f"Pedido para criação: {pedido}")
            return pedido_service.create_pedido(db, pedido)
        except Exception as ex:
            log.error(f"Erro ao criar pedido. {str(ex)}")
            raise HTTPException(status_code=400, detail="Erro ao criar pedido")
    else:
        return "Erro"

@router.get("/", response_model=list[PedidoModel], description="Busca todos os pedidos")
def read_all_pedidos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        log.info("Buscando pedidos")
        pedidos = pedido_service.get_pedidos(db, skip, limit)
        if not pedidos:
            raise HTTPException(status_code=404, detail="Pedidos não encontrados")
        return pedidos
    except HTTPException:
        raise
    except Exception as ex:
        log.error(f"Erro ao buscar pedidos. {str(ex)}")
        raise HTTPException(status_code=400, detail="Erro ao buscar pedidos")


@router.get(
    "/status/{status}",
    response_model=list[PedidoModel],
    description="Busca pedidos por status",
)
def read_pedidos_by_status(
    status: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    try:
        log.info(f"Buscando pedidos com status {status}")
        pedidos = pedido_service.get_pedidos_by_status(db, status, skip, limit)
        if not pedidos:
            raise HTTPException(
                status_code=404, detail=f"Pedidos não encontrados com o status {status}"
            )
        return pedidos
    except HTTPException:
        raise
    except Exception as ex:
        log.error(f"Erro ao buscar pedidos. {str(ex)}")
        raise HTTPException(status_code=400, detail="Erro ao buscar pedidos")


@router.get(
    "/preparacao",
    response_model=list[PedidoModel],
    description="Listar todos os pedidos Em Preparação",
)
def read_pedidos_by_status_em_preparacao(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    try:
        log.info("Buscando pedidos com status 2")
        pedidos = pedido_service.get_pedidos_by_status(
            db, StatusEnum.EM_PREPARACAO.value, skip, limit
        )
        if not pedidos:
            raise HTTPException(
                status_code=404, detail="Pedidos não encontrados com o status 2"
            )
        return pedidos
    except HTTPException:
        raise
    except Exception as ex:
        log.error(f"Erro ao buscar pedidos. {str(ex)}")
        raise HTTPException(status_code=400, detail="Erro ao buscar pedidos")


@router.put(
    "/checkout/{pedido_id}",
    description="Atualiza o status do pedido para 'Em preparação'",
)
def update_pedido_to_preparation(pedido_id: int, db: Session = Depends(get_db)):
    try:
        log.info(f"Atualizando status do pedido {pedido_id} para 'Em preparação'")
        success = pedido_service.atualizar_status_para_preparacao(db, pedido_id)
        if not success:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        return {"message": "Pedido atualizado com sucesso!"}
    except HTTPException:
        raise
    except Exception as ex:
        log.error(f"Erro ao atualizar status do pedido. {str(ex)}")
        raise HTTPException(
            status_code=400, detail="Erro ao atualizar status do pedido"
        )
