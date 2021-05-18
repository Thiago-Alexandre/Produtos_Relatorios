from API_Products.controllers.author_controller import *
from unittest import mock, TestCase


class TestAuthor(TestCase):

    @mock.patch("API_Products.controllers.author_controller.country_db")
    @mock.patch("API_Products.controllers.author_controller.author_db")
    def test_author_insert_validation_works(self,mock_author_db, mock_country_db):
        mock_country_db.search_country.return_value = False
        result = author_insert_validation(dict(name="test",country="test"))
        self.assertEqual(result, {'status': 400, 'text': 'O país não foi encontrado!'})

        mock_country_db.search_country.return_value = False
        result = author_insert_validation(dict())
        self.assertEqual(result, {'status': 400, 'text': 'country'})

        mock_country_db.search_country.return_value = True
        mock_author_db.insert_author_db.return_value = "success"
        result = author_insert_validation(dict(name="test",country="test"))
        self.assertEqual(result, {'status': 200, 'text':"success"})

    @mock.patch("API_Products.controllers.author_controller.author_db")
    def test_author_read_all_validation_works(self, mock_author_db):
        mock_author_db.read_all_authors_db.return_value="success"
        result = author_read_all_validation()
        self.assertEqual(result, {'status': 200, 'text': "success"})

        delattr(mock_author_db, "read_all_authors_db")
        result = author_read_all_validation()
        self.assertEqual(result, {'status': 400, 'text': 'read_all_authors_db'})


    @mock.patch("API_Products.controllers.author_controller.author_db")
    def test_delete_author_works(self, mock_author_db):
        mock_author_db.exist_author.return_value = False
        mock_author_db.delete_authors_db.return_value = "success"
        result = delete_author(dict(test="test"))
        self.assertEqual(result, {'status': 200, 'text': "success"})

        mock_author_db.exist_author.return_value = True
        result = delete_author(dict(test="test"))
        self.assertEqual(result, {'status': 400, 'text': 'O autor já está sendo utilizado, não é possível deletá-lo agora.'})
