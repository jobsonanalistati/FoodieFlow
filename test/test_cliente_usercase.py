import pytest
from unittest.mock import Mock, patch
from core.model.cliente import Cliente as ClienteModel
from core.ports.cliente_repository import ClienteRepository
from core.usecases.cliente_service_impl import ClienteServiceImpl
from sqlalchemy.orm import Session


# Cenário: Criar cliente
def test_create_cliente():
    # Dado que temos um cliente e um repositório mock
    cliente = ClienteModel(cpf="123.456.789-00")
    repo_mock = Mock(spec=ClienteRepository)
    repo_mock.get_cliente_by_cpf.return_value = None
    service = ClienteServiceImpl(cliente_repository=repo_mock)
    session = Session()

    # Quando tentamos criar o cliente
    result = service.create_cliente(session, cliente)

    # Então o método create_cliente do repositório deve ser chamado com o cliente correto
    repo_mock.create_cliente.assert_called_once_with(session, cliente)


# Cenário: Obter cliente
def test_get_cliente():
    # Dado que temos um repositório mock
    repo_mock = Mock(spec=ClienteRepository)
    service = ClienteServiceImpl(cliente_repository=repo_mock)
    session = Session()

    # Quando tentamos obter um cliente
    service.get_cliente(session, 1)

    # Então o método get_cliente do repositório deve ser chamado com o id correto
    repo_mock.get_cliente.assert_called_once_with(session, 1)
