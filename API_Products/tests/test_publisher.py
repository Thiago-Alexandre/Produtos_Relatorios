from API_Products.controllers.publisher_controller import *
from unittest import mock, TestCase


class TestPublisher(TestCase):

    @mock.patch("API_Products.controllers.publisher_controller.country_db")
    @mock.patch("API_Products.controllers.publisher_controller.publisher_db")
    def test_insert_publisher_works(self, mock_publisher, mock_country):
            mock_country.search_country.side_effect = [False, True, True]
            mock_publisher.insert_publishers_db.return_value = "Success"

            result = insert_publisher(dict(name="test", country="test"))
            result2 = insert_publisher(dict(name="test", country="test"))
            result3 = insert_publisher(dict())

            expected = dict(status=400, error="País não foi encontrado!", message="Verifique os dados informados.")
            expected2 = dict(status=200, result_data="Success")
            expected3 = dict(status=400, error="Valores inseridos inválidos.", message="Verifique os dados informados.")

            self.assertEqual(result, expected)
            self.assertEqual(result2, expected2)
            self.assertEqual(result3, expected3)


    # ===================================================================================

    @mock.patch("API_Products.controllers.publisher_controller.publisher_db")
    def test_read_all_publisher_works(self, mock_publisher):
        mock_publisher.read_all_publishers_db.return_value = []

        result = read_all_publishers()
        delattr(mock_publisher, "read_all_publishers_db")
        result2 = read_all_publishers()

        expected = dict(status=200, result_data=[])
        expected2 = dict(status=400, error="read_all_publishers_db", message="Tente novamente mais tarde.")

        self.assertEqual(result, expected)
        self.assertEqual(result2, expected2)
    
    # ===================================================================================

    @mock.patch("API_Products.controllers.publisher_controller.book_db")
    @mock.patch("API_Products.controllers.publisher_controller.publisher_db")
    def test_update_publisher_db_works(self, mock_publisher, mock_book):
        mock_publisher.validate_publisher.return_value = False
        mock_publisher.update_publisher_db.return_value = "Success"
        mock_book.update_all_publishers_book_db.return_value = "Success"

        result = update_publisher(dict(name="", new_value=""))
        self.assertEqual(result, {'status': 200, 'text': 'Success'})

        mock_publisher.validate_publisher.return_value = True
        result = update_publisher(dict(name="", new_value=""))
        self.assertEqual(result, {'status': 400, 'text': 'O nome requerido já está sendo utilizado, não é possível atribuí-lo novamente.'})
    
    # ===================================================================================

    @mock.patch("API_Products.controllers.publisher_controller.publisher_db")
    def test_delete_publisher(self, mock_publisher):
        mock_publisher.exists_publisher.return_value = False
        mock_publisher.delete_publishers_db.return_value = "Success"

        result = delete_publisher(dict())
        self.assertEqual(result, {'status': 200, 'text': 'Success'})

        mock_publisher.exists_publisher.return_value = True
        result = delete_publisher(dict())
        self.assertEqual(result, {'status': 400, 'text': 'A editora está sendo utilizada, não é possível deletá-la.'})
        