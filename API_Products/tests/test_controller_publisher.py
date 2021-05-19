from controllers.publisher_controller import *
from unittest import mock, TestCase
from unittest.mock import Mock


class TestPublisher(TestCase):

    @mock.patch("controllers.publisher_controller.publisher_db")
    @mock.patch("controllers.publisher_controller.country_db")
    def test_insert_publisher_works(self, mock_country, mock_publisher):
        result_data = insert_publisher(dict())
        self.assertEqual(result_data, dict(status=400, error="Valores inseridos inválidos.",
                                           message="Verifique os dados informados."))

        mock_country.search_country.return_value = False
        expected = dict(status=400, error="País não foi encontrado!", message="Verifique os dados informados.")
        result_data = insert_publisher(dict(name="test", country="test"))
        self.assertEqual(result_data, expected)

        mock_country.search_country.return_value = True
        mock_publisher.insert_publishers_db.return_value = "Editora salva com sucesso!"

        expected = dict(status=200, result_data="Editora salva com sucesso!")
        result_data = insert_publisher(dict(name="test", country="test"))
        self.assertEqual(result_data, expected)

        mock_publisher.insert_publishers_db.side_effect = Exception("Ocorreu um erro ao salvar a editora.")
        expected = dict(status=400, error="Ocorreu um erro ao salvar a editora.",
                        message="Verifique os dados informados.")
        result_data = insert_publisher(dict(name="teste", country="teste"))
        self.assertEqual(result_data, expected)

    def test_read_all_publisher_works(self):
        with mock.patch("controllers.publisher_controller.publisher_db") as mock_publisher:
            mock_publisher.read_all_publishers_db.return_value = [dict(teste="teste"), dict(teste="teste")]
            expected = dict(status=200, result_data=[dict(teste="teste"), dict(teste="teste")])
            result = read_all_publishers()
            self.assertEqual(result, expected)

        with mock.patch("controllers.publisher_controller.publisher_db") as mock_publisher:
            mock_publisher.read_all_publishers_db = Mock(side_effect=
                                                         Exception("Nenhuma editora encontrada!"))
            expected = dict(status=400, error="Nenhuma editora encontrada!", message="Tente novamente mais tarde.")
            result = read_all_publishers()
            self.assertEqual(result, expected)

    @mock.patch("controllers.publisher_controller.publisher_db.update_publisher_db")
    @mock.patch("controllers.publisher_controller.publisher_db.validate_publisher")
    @mock.patch("controllers.publisher_controller.book_db")
    @mock.patch("controllers.publisher_controller.publisher_db.search_publisher")
    def test_update_publisher_db_works(self, mock_search_publisher, mock_book, mock_validate_publisher,
                                       mock_update_publisher):
        mock_search_publisher.return_value = dict(name="")
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

        mock_publisher.exists_publisher.return_value = True
        expected = dict(status=400, message="Verifique os dados informados.",
                       error="A editora está sendo utilizada, não é possível deletá-la.")
        result_data = delete_publisher(dict())
        self.assertEqual(result_data, expected)

        mock_publisher.exists_publisher.return_value = False
        mock_publisher.delete_publishers_db.return_value = "Editora excluída com sucesso!"
        expected = dict(status=200, result_data="Editora excluída com sucesso!")
        result_data = delete_publisher(dict())
        self.assertEqual(result_data, expected)

        mock_publisher.delete_publishers_db.side_effect = Exception("Nenhuma editora encontrada!")
        mock_publisher.delete_publishers_db.return_value = "Editora excluída com sucesso!"
        expected = dict(status=400, error="Nenhuma editora encontrada!", message="Verifique os dados informados.")
        result_data = delete_publisher(dict())
        self.assertEqual(result_data, expected)
