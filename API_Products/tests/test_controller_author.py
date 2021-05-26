from controllers.author_controller import *
from unittest import mock, TestCase
from unittest.mock import Mock


class TestAuthor(TestCase):

    @mock.patch("controllers.author_controller.author_db")
    @mock.patch("controllers.author_controller.country_db")
    def test_insert_author_works(self, mock_country, mock_author):
        """
        Testes do método controller de cadastrar novo autor.

        :param mock_country:
        :param mock_author:
        :return:
        """
        # Testa a verificação dos dados enviados válidos.
        result_data = insert_author(dict())
        self.assertEqual(result_data, dict(status=400, error="Valores inseridos inválidos.",
                                           message="Verifique os dados informados."))
        result_data = insert_author(dict(_id="Teste", name="Teste", country="Teste"))
        self.assertEqual(result_data, dict(status=400, error="Valores inseridos inválidos.",
                                           message="Verifique os dados informados."))

        # Testa a verificação do autor já cadastrado.
        mock_author.validate_author.return_value = True
        result_data = insert_author(dict(name="test", lastname="test", country="test"))
        self.assertEqual(result_data, dict(status=400, error="Autor já salvo!",
                                           message="Verifique os dados informados."))

        # Testa a verificação do país cadastrado.
        mock_author.validate_author.return_value = False
        mock_country.search_country.return_value = False
        result_data = insert_author(dict(name="test", lastname="test", country="test"))
        self.assertEqual(result_data, dict(status=400, error="País não foi encontrado!",
                                           message="Verifique os dados informados."))

        # Testa o salvar autor.
        mock_country.search_country.return_value = True
        mock_author.insert_author_db.return_value = "Autor salvo com sucesso!"
        result_data = insert_author(dict(name="test", lastname="test", country="test"))
        self.assertEqual(result_data, dict(status=200, result_data="Autor salvo com sucesso!"))

        # Testa o lançamento de exceções
        mock_author.insert_author_db.side_effect = Exception("Ocorreu um erro ao salvar o autor.")
        result_data = insert_author(dict(name="test", lastname="test", country="test"))
        self.assertEqual(result_data, dict(status=400, error="Ocorreu um erro ao salvar o autor.",
                                           message="Verifique os dados informados."))

    @mock.patch("controllers.author_controller.author_db")
    def test_read_all_author_works(self, mock_author):
        """
        Teste do método controller de pesquisar as editoras salvas.
        :param mock_author:
        :return:
        """
        # Teste de retorno dos dados pesquisados.
        mock_author.read_all_authors_db.return_value = [dict(teste="teste"), dict(teste="teste")]
        result = read_all_authors()
        self.assertEqual(result, dict(status=200, result_data=[dict(teste="teste"), dict(teste="teste")]))

        # Teste de lançamento de exceções.
        mock_author.read_all_authors_db = Mock(side_effect=Exception("Nenhum autor encontrado!"))
        result = read_all_authors()
        self.assertEqual(result, dict(status=400, error="Nenhum autor encontrado!",
                                      message="Tente novamente mais tarde."))

    @mock.patch("controllers.author_controller.book_db")
    @mock.patch("controllers.author_controller.country_db")
    @mock.patch("controllers.author_controller.author_db")
    def test_update_author_db_works(self, mock_author, mock_country, mock_book):
        """
        Teste do método controller para alterar dados dos autores.

        :param mock_author:
        :param mock_book:
        :return:
        """

        # Testa a verificação dos dados enviados válidos.
        result_data = update_author(dict())
        self.assertEqual(result_data, dict(status=400, error="Valores inseridos inválidos.",
                                           message="Verifique os dados informados."))
        result_data = update_author(dict(_id="Teste", name="Teste", lastname="Teste", country="Teste",
                                         novo_campo="Teste"))
        self.assertEqual(result_data, dict(status=400, error="Valores inseridos inválidos.",
                                           message="Verifique os dados informados."))

        # Testa a verificação de autor já salvo.
        mock_author.validate_author.return_value = True
        result_data = update_author(dict(_id="Teste", name="Teste", lastname="Teste", country="Teste"))
        self.assertEqual(result_data, dict(status=400, error="Autor já salvo!",
                                           message="Verifique os dados informados."))

        # Testa a verificação de país cadastrado.
        mock_author.validate_author.return_value = False
        mock_country.search_country.return_value = False
        result_data = update_author(dict(_id="Teste", name="Teste", lastname="Teste", country="Teste"))
        self.assertEqual(result_data, dict(status=400, error="País não foi encontrado!",
                                           message="Verifique os dados informados."))

        # Testa a alteração do autor.
        mock_country.search_country.return_value = True
        mock_author.search_author.return_value = True
        mock_author.update_author_db.return_value = "Autor alterado com sucesso!"
        mock_book.update_all_authors_book_db.return_value = True
        result_data = update_author(dict(_id="Teste", name="Teste", lastname="Teste", country="Teste"))
        self.assertEqual(result_data, dict(status=200, result_data="Autor alterado com sucesso!"))

        # Testa o lançamento de exceções
        mock_author.update_author_db.side_effect = Exception("Ocorreu um erro ao alterar o autor.")
        result_data = update_author(dict(_id="Teste", name="Teste", lastname="Teste", country="Teste"))
        self.assertEqual(result_data, dict(status=400, error="Ocorreu um erro ao alterar o autor.",
                                           message="Verifique os dados informados."))

    @mock.patch("controllers.author_controller.author_db")
    def test_delete_author(self, mock_author):
        """
        Teste do método controller de excluir autor.

        :param mock_author:
        :return:
        """
        # Testa a verificação do autor sendo utilizado em algum livro salvo.
        mock_author.exists_author.return_value = True
        result_data = delete_author(dict())
        self.assertEqual(result_data, dict(status=400, message="Verifique os dados informados.",
                                           error="O autor está sendo utilizado, não é possível deletá-lo."))

        # Testa a exclusão do autor.
        mock_author.exists_author.return_value = False
        mock_author.delete_authors_db.return_value = "Autor excluído com sucesso!"
        result_data = delete_author(dict())
        self.assertEqual(result_data, dict(status=200, result_data="Autor excluído com sucesso!"))

        # Testa o lançamento de exceções
        mock_author.delete_authors_db.side_effect = Exception("Ocorreu um erro ao excluir o autor!")
        result_data = delete_author(dict())
        self.assertEqual(result_data, dict(status=400, error="Ocorreu um erro ao excluir o autor!",
                                           message="Verifique os dados informados."))
