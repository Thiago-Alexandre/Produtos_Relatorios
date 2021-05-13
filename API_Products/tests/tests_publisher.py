from API_Products.database.publisher_db import *
from unittest import mock, TestCase

class TestDataBase(TestCase):
    
    @mock.patch("API_Products.database.publisher_db.insert.dict_values")
    def test_insert_works(self, mock_values):
        mock_values.return_values = {}
        result = insert({})

        self.assertEqual(result, {})


