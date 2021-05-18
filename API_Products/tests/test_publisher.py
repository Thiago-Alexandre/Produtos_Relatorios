from API_Products.controllers.publisher_controller import *
from unittest import mock, TestCase


class TestPublisher(TestCase):

    @mock.patch("API_Products.controllers.publisher_controller.country_db")
    @mock.patch("API_Products.controllers.publisher_controller.publisher_db")
    def test_insert_publisher_works(self, mock_publisher, mock_country):

            mock_country.search_country.return_value = False

            result = insert_publisher(dict(name="test", country="test"))
            self.assertEqual(result, {'status': 400, 'text': 'País não foi encontrado!'})

            mock_country.search_country.return_value = True
            mock_publisher.insert_publishers_db.return_value = "Success"
            result2 = insert_publisher(dict(name="test", country="test"))
            self.assertEqual(result2, {'status': 200, 'text': "Success"})

            result3 = insert_publisher(dict())
            self.assertEqual(result3, {'status': 400, 'text': 'country'})

    # ===================================================================================

    @mock.patch("API_Products.controllers.publisher_controller.publisher_db")
    def test_read_all_publisher_works(self, mock_publisher):
        mock_publisher.read_all_publishers_db.return_value = []

        result = read_all_publishers()
        self.assertEqual(result, dict(status=200, text=[]))

        delattr(mock_publisher, "read_all_publishers_db")
        result2 = read_all_publishers()
        self.assertEqual(result2, dict(status=400, text="read_all_publishers_db"))
    
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
        