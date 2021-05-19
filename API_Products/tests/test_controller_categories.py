from unittest import mock, TestCase
from controllers.category import *


class TestControllerCategories(TestCase):
    @mock.patch("controllers.category.category_db")
    def test_read_all_categories_works(self, mock_category):
        mock_category.read_all_categories_db.return_value = []

        result = read_all_categories()
        self.assertEqual(result, dict(status=200, result_data=[]))

        delattr(mock_category, "read_all_categories_db")
        result2 = read_all_categories()
        self.assertEqual(result2, dict(status=500, error="Nenhuma categoria foi encontrada.", message="Tente novamente mais tarde."))

    @mock.patch("controllers.category.get_db")
    @mock.patch("controllers.category.category_db")
    def test_insert_categories_works(self, mock_category, mock_db):
        result1 = insert_categories(dict(name=""))
        self.assertEqual(result1, dict(status=400, error="Valor inserido inválido.", message="Verifique os dados informados."))

        mock_db()["category"].count_documents.side_effect = [0, 0, 1]

        result2 = insert_categories(dict(name="A"))
        self.assertEqual(result2, dict(status=200, message="Cadastrado com sucesso."))

        delattr(mock_category, "insert_categories_db")
        result3 = insert_categories(dict(name="A"))
        self.assertEqual(result3, dict(
                status=400,
                error=f"Categoria não cadastrada: insert_categories_db.",
                message="Verifique a categoria informada!"
            ))

        result4 = insert_categories(dict(name="A"))
        self.assertEqual(result4, dict(status=400, error="Categoria não cadastrada.",
                                       message="A categoria já existe no sistema."))

    @mock.patch("controllers.category.category_db")
    @mock.patch("controllers.category.get_db")
    def test_delete_categories_works(self, mock_find, mock_category_db):
        result1 = delete_categories(dict(name=""))
        self.assertEqual(result1,
                         dict(status=400, error="Valor inserido inválido.", message="Verifique os dados informados."))

        mock_find()["category"].find_one.side_effect = [True, False, False]

        result2 = delete_categories(dict(name="A"))
        self.assertEqual(result2, dict(status=400, error="A categoria está sendo utilizada.", message="Não é possível deletá-la."))

        mock_category_db.delete_categories_db.side_effect = [1, 0]

        result3 = delete_categories(dict(name="A"))
        self.assertEqual(result3, dict(status=200, message="Categoria deletada com sucesso."))

        result4 = delete_categories(dict(name="A"))
        self.assertEqual(result4, dict(status=500, error="Erro interno.", message="A categoria não foi deletada."))

    @mock.patch("controllers.category.category_db")
    @mock.patch("controllers.category.get_db")
    def test_update_categories_works(self, mock_get_db, mock_category_db):
        result1 = update_categories(dict(old_name="", new_name=""))
        self.assertEqual(result1,
                         dict(status=400, error="Valor inserido inválido.", message="Verifique os dados informados."))

        mock_get_db()["category"].find_one.side_effect = [True, False, False]

        result2 = update_categories(dict(new_name="B", old_name="A"))
        expected = dict(status=400, erro="Já existe uma categoria com este nome.",
                        message="Verifique os dados informados.")
        self.assertEqual(result2, expected)

        mock_category_db.update_categories_db.side_effect = [False, True]
        result3 = update_categories(dict(old_name="A", new_name="B"))
        self.assertEqual(result3, dict(status=500, error="Erro interno.", message="A categoria não foi modificada."))

        result4 = update_categories(dict(old_name="A", new_name="B"))
        self.assertEqual(result4, dict(status=200, message="Categoria alterada com sucesso."))
