from API_Products.database.publisher_db import *
from unittest import mock, TestCase

class TestDataBase(TestCase):
    
    @mock.patch("API_Products.database.publisher_db.insert")
    def test_insert_works(self, mock_values):
        mock_values.dict_values.return_values = {}
        result = insert(dict(name=""))
        self.assertEqual(result, result)

        with self.assertRaises(Exception) as error:
            insert(dict())

        self.assertEqual("Registro inválido.", error.exception.args[0])

    @mock.patch("API_Products.database.publisher_db.read_all")
    def test_read_all_works(self, mock_values):
        mock_values.publishers_list.return_values = []
        result = read_all()

        self.assertEqual(result, [])








