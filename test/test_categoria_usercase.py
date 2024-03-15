import unittest
from unittest.mock import Mock
from core.model.categoria import Categoria as CategoriaModel
from core.ports.categoria_repository import CategoriaRepository
from core.usecases.categoria_service_impl import CategoriaServiceImpl
from sqlalchemy.orm import Session


class TestCategoria(unittest.TestCase):

    # Cenário: Criar categoria
    def test_create_categoria(self):
        # Dado que temos uma categoria e um repositório mock
        categoria = CategoriaModel(nome="Teste")
        repo_mock = Mock(spec=CategoriaRepository)
        repo_mock.get_categoria_by_nome.return_value = None
        service = CategoriaServiceImpl(categoria_repository=repo_mock)
        session = Session()

        # Quando tentamos criar a categoria
        result = service.create_categoria(session, categoria)

        # Então o método create_categoria do repositório deve ser chamado com a categoria correta
        repo_mock.create_categoria.assert_called_once_with(session, categoria)

    # Cenário: Obter categoria
    def test_get_categoria(self):
        # Dado que temos um repositório mock
        repo_mock = Mock(spec=CategoriaRepository)
        service = CategoriaServiceImpl(categoria_repository=repo_mock)
        session = Session()

        # Quando tentamos obter uma categoria
        service.get_categoria(session, 1)

        # Então o método get_categoria do repositório deve ser chamado com o id correto
        repo_mock.get_categoria.assert_called_once_with(session, 1)


if __name__ == "__main__":
    unittest.main()
