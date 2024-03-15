import unittest
from unittest.mock import Mock
from core.model.pedido import Pedido as PedidoModel
from core.ports.pedido_repository import PedidoRepository
from core.usecases.pedido_service_impl import PedidoServiceImpl
from sqlalchemy.orm import Session


class TestPedido(unittest.TestCase):

    # Cenário: Criar pedido
    def test_create_pedido(self):
        # Dado que temos um pedido e um repositório mock
        pedido = PedidoModel(
            id=1, codigo="codigo", id_cliente=1, id_status=0, produtos=[]
        )
        repo_mock = Mock(spec=PedidoRepository)
        service = PedidoServiceImpl(pedido_repository=repo_mock)
        session = Session()

        # Quando tentamos criar o pedido
        result = service.create_pedido(session, pedido)

        # Então o método create_pedido do repositório deve ser chamado com o pedido correto
        repo_mock.create_pedido.assert_called_once_with(session, pedido)

    # Cenário: Obter pedidos
    def test_get_pedidos(self):
        # Dado que temos um repositório mock
        repo_mock = Mock(spec=PedidoRepository)
        service = PedidoServiceImpl(pedido_repository=repo_mock)
        session = Session()

        # Quando tentamos obter os pedidos
        service.get_pedidos(session)

        # Então o método get_pedidos do repositório deve ser chamado
        repo_mock.get_pedidos.assert_called_once_with(session, 0, 100)


if __name__ == "__main__":
    unittest.main()
