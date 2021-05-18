from API_Products.controllers.author_controller import *
from unittest import mock, TestCase


class TestAuthor(TestCase):

    @mock.patch("API_Products.controllers.author_controller.author_db")
    @mock.patch("API_Products.controllers.author_controller.country_db")
    def test_author_insert_validation_works(self, mock_country_db, mock_author_db):

        result = author_insert_validation({"teste": "teste"})
        self.assertEqual(result, {"status": 400, "error": "Valores inseridos inválidos.",
                                  "message": "Verifique os dados informados."})

        result = author_insert_validation({"name": "", "lastname": "", "country": ""})
        self.assertEqual(result, {"status": 400, "error": "Valores inseridos inválidos.",
                                  "message": "Verifique os dados informados."})

        mock_country_db.search_country.return_value = ""
        result = author_insert_validation({"name": "teste", "lastname": "teste", "country": "teste"})
        self.assertEqual(result, dict(status=400, error="O país não foi encontrado!",
                                      message="Verifique o dados informados."))

        mock_country_db.search_country.return_value = "teste"
        mock_author_db.insert_author_db.return_value = "success"
        result = author_insert_validation({"name": "teste", "lastname": "teste", "country": "teste"})
        self.assertEqual(result, {'status': 200, 'result_data': "success"})

    @mock.patch("API_Products.controllers.author_controller.author_db")
    def test_author_read_all_validation_works(self, mock_author_db):
        mock_author_db.read_all_authors_db.return_value="success"
        result = author_read_all_validation()
        self.assertEqual(result, {'result_data': 'success', 'status': 200})

        delattr(mock_author_db, "read_all_authors_db")
        result = author_read_all_validation()
        self.assertEqual(result, {'error': 'read_all_authors_db',
                                  'message': 'Tente novamente mais tarde.',
                                  'status': 400})

    @mock.patch("API_Products.controllers.author_controller.author_db")
    def test_delete_author_works(self, mock_author_db):
        mock_author_db.exist_author.return_value = False
        mock_author_db.delete_authors_db.return_value = "success"
        result = delete_author(dict(test="test"))
        self.assertEqual(result, {'result_data': 'success', 'status': 200})

        mock_author_db.exist_author.return_value = True
        result = delete_author(dict(test="test"))
        self.assertEqual(result, {'error': 'Não foi possível deletar o autor.',
                                  'message': 'O autor já está sendo utilizado.',
                                  'status': 400})
