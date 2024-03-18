import pytest
from unittest.mock import Mock, patch
from core.model.produto import Produto as ProdutoModel
from core.ports.produto_repository import ProdutoRepository
from core.usecases.produto_service_impl import ProdutoServiceImpl
from sqlalchemy.orm import Session


# Cenário: Criar produto
def test_create_produto():
    # Dado que temos um produto e um repositório mock
    produto = ProdutoModel(id=1, nome="Produto Teste", preco=10.0, id_categoria=1)
    repo_mock = Mock(spec=ProdutoRepository)
    service = ProdutoServiceImpl(produto_repository=repo_mock)
    session = Session()

    # Quando tentamos criar o produto
    result = service.create_produto(session, produto)

    # Então o método create_produto do repositório deve ser chamado com o produto correto
    repo_mock.create_produto.assert_called_once_with(session, produto)


# Cenário: Obter produto
def test_get_produto():
    # Dado que temos um repositório mock
    repo_mock = Mock(spec=ProdutoRepository)
    service = ProdutoServiceImpl(produto_repository=repo_mock)
    session = Session()

    # Quando tentamos obter um produto
    service.get_produto(session, 1)

    # Então o método get_produto do repositório deve ser chamado com o id correto
    repo_mock.get_produto.assert_called_once_with(session, 1)
    
