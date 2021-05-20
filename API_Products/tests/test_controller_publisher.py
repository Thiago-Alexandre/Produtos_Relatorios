from controllers.publisher_controller import *
from unittest import mock, TestCase
from unittest.mock import Mock


class TestPublisher(TestCase):

    @mock.patch("controllers.publisher_controller.publisher_db")
    @mock.patch("controllers.publisher_controller.country_db")
    def test_insert_publisher_works(self, mock_country, mock_publisher):
        """
        Testes do método controller de cadastrar nova editora.

        :param mock_country:
        :param mock_publisher:
        :return:
        """
        # Testa a verificação dos dados enviados válidos.
        result_data = insert_publisher(dict())
        self.assertEqual(result_data, dict(status=400, error="Valores inseridos inválidos.",
                                           message="Verifique os dados informados."))
        result_data = insert_publisher(dict(_id="Teste", name="Teste", country="Teste"))
        self.assertEqual(result_data, dict(status=400, error="Valores inseridos inválidos.",
                                           message="Verifique os dados informados."))

        # Testa a verificação da editora já cadastrada.
        mock_publisher.validate_publisher.return_value = True
        result_data = insert_publisher(dict(name="test", country="test"))
        self.assertEqual(result_data, dict(status=400, error="Editora já salva!",
                                           message="Verifique os dados informados."))

        # Testa a verificação do país cadastrado.
        mock_publisher.validate_publisher.return_value = False
        mock_country.search_country.return_value = False
        result_data = insert_publisher(dict(name="test", country="test"))
        self.assertEqual(result_data, dict(status=400, error="País não foi encontrado!",
                                           message="Verifique os dados informados."))

        # Testa o salvar editora.
        mock_country.search_country.return_value = True
        mock_publisher.insert_publishers_db.return_value = "Editora salva com sucesso!"
        result_data = insert_publisher(dict(name="test", country="test"))
        self.assertEqual(result_data, dict(status=200, result_data="Editora salva com sucesso!"))

        # Testa o lançamento de exceções
        mock_publisher.insert_publishers_db.side_effect = Exception("Ocorreu um erro ao salvar a editora.")
        result_data = insert_publisher(dict(name="teste", country="teste"))
        self.assertEqual(result_data, dict(status=400, error="Ocorreu um erro ao salvar a editora.",
                                           message="Verifique os dados informados."))

    @mock.patch("controllers.publisher_controller.publisher_db")
    def test_read_all_publisher_works(self, mock_publisher):
        """
        Teste do método controller de pesquisar as editoras salvas.
        :param mock_publisher:
        :return:
        """
        # Teste de retorno dos dados pesquisados.
        mock_publisher.read_all_publishers_db.return_value = [dict(teste="teste"), dict(teste="teste")]
        result = read_all_publishers()
        self.assertEqual(result, dict(status=200, result_data=[dict(teste="teste"), dict(teste="teste")]))

        # Teste de lançamento de exceções.
        mock_publisher.read_all_publishers_db = Mock(side_effect=Exception("Nenhuma editora encontrada!"))
        result = read_all_publishers()
        self.assertEqual(result, dict(status=400, error="Nenhuma editora encontrada!",
                                      message="Tente novamente mais tarde."))

    @mock.patch("controllers.publisher_controller.book_db")
    @mock.patch("controllers.publisher_controller.publisher_db")
    def test_update_publisher_db_works(self, mock_publisher, mock_book):
        """
        Teste do método controller para alterar dados das editoras.

        :param mock_publisher:
        :param mock_book:
        :return:
        """

        # Testa a verificação dos dados enviados válidos.
        result_data = update_publisher(dict())
        self.assertEqual(result_data, dict(status=400, error="Valores inseridos inválidos.",
                                           message="Verifique os dados informados."))
        result_data = update_publisher(dict(_id="Teste", name="Teste", country="Teste", novo_campo="Teste"))
        self.assertEqual(result_data, dict(status=400, error="Valores inseridos inválidos.",
                                           message="Verifique os dados informados."))

        # Testa a verificação de editora já salva.
        mock_publisher.search_publisher.return_value = dict(name="")
        mock_book.update_all_publishers_book_db.return_value = True

        expected = dict(status=400, error="Valores inseridos inválidos.", message="Verifique os dados informados.")
        result_data = insert_publisher(dict())
        self.assertEqual(result_data, expected)

        mock_validate_publisher.side_effect = [True, False, False]

        expected = dict(status=400, message="Verifique os dados informados.",
                        error="O nome requerido já está sendo utilizado, não é possível atribuí-lo novamente.")
        result_data = update_publisher(dict(_id="teste", name="test", country="test"))
        self.assertEqual(result_data, expected)

        mock_update_publisher.return_value = "Editora alterada com sucesso!"
        expected = dict(status=200, result_data="Editora alterada com sucesso!")
        result_data = update_publisher(dict(_id="teste", name="test", country="test"))
        self.assertEqual(result_data, expected)

        mock_update_publisher.side_effect = Exception("Nenhuma editora encontrada!")
        expected = dict(status=400, error="Nenhuma editora encontrada!", message="Verifique os dados informados.")
        result_data = update_publisher(dict(_id="teste", name="test", country="test"))
        self.assertEqual(result_data, expected)

    @mock.patch("controllers.publisher_controller.publisher_db")
    def test_delete_publisher(self, mock_publisher):
        """
        Teste do método controller de excluir editora.

        :param mock_publisher:
        :return:
        """
        # Testa a verificação da editora sendo utilizada em algum livro salvo.
        mock_publisher.exists_publisher.return_value = True
        result_data = delete_publisher(dict())
        self.assertEqual(result_data, dict(status=400, message="Verifique os dados informados.",
                                           error="A editora está sendo utilizada, não é possível deletá-la."))

        # Testa a exclusão da editora.
        mock_publisher.exists_publisher.return_value = False
        mock_publisher.delete_publishers_db.return_value = "Editora excluída com sucesso!"
        result_data = delete_publisher(dict())
        self.assertEqual(result_data, dict(status=200, result_data="Editora excluída com sucesso!"))

        # Testa o lançamento de exceções
        mock_publisher.delete_publishers_db.side_effect = Exception("Nenhuma editora encontrada!")
        result_data = delete_publisher(dict())
        self.assertEqual(result_data, dict(status=400, error="Nenhuma editora encontrada!",
                                           message="Verifique os dados informados."))
