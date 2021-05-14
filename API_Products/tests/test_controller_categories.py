from unittest import mock,TestCase
from API_Products.controllers.category import *


class TestControllerCategories(TestCase):
    @mock.patch("API_Products.controllers.category.category_db")
    def test_read_all_categories_works(self, mock_category):
        mock_category.read_all_categories_db.return_value = []

        result = read_all_categories()
        self.assertEqual(result, dict(status=200, text=[]))

        delattr(mock_category, "read_all_categories_db")
        result2 = read_all_categories()
        self.assertEqual(result2, dict(status=400, text="read_all_categories_db"))

    @mock.patch("API_Products.controllers.category.db")
    @mock.patch("API_Products.controllers.category.category_db")
    def test_insert_categories_works(self, mock_category, mock_db):
        mock_db.DB["category"].count_documents.side_effect = [0, 0, 1]

        result = insert_categories(dict(name="A"))
        self.assertEqual(result, dict(status=200, text="Cadastrado com sucesso."))

        delattr(mock_category, "insert_categories_db")
        result2 = insert_categories(dict(name="A"))
        self.assertEqual(result2, dict(status=400, text=f"Não foi possível cadastrar a categoria.insert_categories_db"))

        result3 = insert_categories(dict(name="A"))
        self.assertEqual(result3, dict(status=400, text="Categoria já cadastrada."))