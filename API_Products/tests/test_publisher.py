from API_Products.controllers.publisher import *
from unittest import mock, TestCase

class TestDataBase(TestCase):


    def test_insert_publisher_works(self):
        with mock.patch("API_Products.controllers.publisher.insert_publisher") as mock_publisher:

            mock_publisher.exist_country.return_values = []

            result = insert_publisher(dict(name="test", country="test"))
            self.assertEqual(result, {'status': 400, 'text': 'País não foi encontrado!'})

        with mock.patch("API_Products.controllers.publisher.insert_publisher") as mock_publisher:

            mock_publisher.exist_country.return_values = [dict()]

            result = insert_publisher(dict())
            self.assertEqual(result, {'status': 400, 'text': 'country'})

            result = insert_publisher(dict(name="test", country="Brasil"))
            self.assertEqual(result, {'status': 200, 'text': 'Registro inserido com sucesso!'})

    @mock.patch("API_Products.controllers.publisher.publisher_db")
    def test_read_all_publisher_works(self, mock_publisher):
        mock_publisher.read_all_publishers_db.return_value = []

        result = read_all_publishers()
        self.assertEqual(result, dict(status=200, text=[]))

        delattr(mock_publisher, "read_all_publishers_db")
        result2 = read_all_publishers()
        self.assertEqual(result2, dict(status=400, text="read_all_publishers_db"))

