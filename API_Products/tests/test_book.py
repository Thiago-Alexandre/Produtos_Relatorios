from builtins import delattr

import controllers.utils
from controllers.book_controller import *
from unittest import mock, TestCase

from controllers.utils import validate_book


class TestBook(TestCase):

    @mock.patch("controllers.book_controller.insert_book_db")
    @mock.patch("controllers.book_controller.validate_book")
    def test_insert_book_works(self, mock_validade_book, mock_insert_book):
        error = "Teste"
        message= "Mensagem"

        mock_validade_book.side_effect = Exception(error, message)
        expected = dict(status=400, error="Teste", message="Mensagem")
        self.assertEqual(insert_book(dict()), expected)

        mock_validade_book.side_effect = [True, True]
        mock_insert_book.side_effect = Exception(error, message)
        expected = dict(status=500, error="Teste", message="Mensagem")
        self.assertEqual(insert_book(dict()), expected)

        mock_insert_book.side_effect = [dict(_id=10)]
        expected = dict(status=200, message="Livro cadastrado com sucesso!", book={'_id': '10'})
        self.assertEqual(insert_book(dict()), expected)

    @mock.patch("controllers.book_controller.update_book_db")
    @mock.patch("controllers.book_controller.validate_book")
    def test_update_book_works(self, mock_validade_book, mock_update_book):
        error = "Teste"
        message = "Mensagem"

        mock_validade_book.side_effect = Exception(error, message)
        expected = dict(status=400, error="Teste", message="Mensagem")
        self.assertEqual(update_book(dict()), expected)

        mock_validade_book.side_effect = [True, True]
        mock_update_book.side_effect = Exception(error, message)
        expected = dict(status=500, error="Teste", message="Mensagem")
        self.assertEqual(update_book(dict()), expected)

        mock_update_book.side_effect = [[dict(_id=10)]]
        expected = dict(status=200, message="Livro atualizado com sucesso!", book={'_id': '10'})
        self.assertEqual(update_book(dict()), expected)

    @mock.patch("controllers.book_controller.read_all_books_db")
    def test_get_book_list(self, mock_read_all_books_db):
        mock_read_all_books_db.side_effect = [[], ["teste", "teste"], Exception("Nenhum livro encontrado!")]
        self.assertEqual(get_book_list(), dict(status=200, message="Nenhum livro cadastrado.", result_data=[]))
        self.assertEqual(get_book_list(), dict(status=200, result_data=["teste", "teste"]))
        self.assertEqual(get_book_list(), dict(status=500, error="Nenhum livro encontrado!",
                                               message="Tente novamente mais tarde."))

    # @mock.patch("controllers.book_controller")
    # @mock.patch("controllers.book_controller.book_db")
    # def test_verify_stock_works(self, mock_book_db, mock_book):
    #     mock_book_db.search_books_by_id.return_value = [{"item_price":1, "item_quantity":10, "page_quantity":1, "format": ""}]
    #
    #     result = verify_stock([dict(quantity_purchased=20)])
    #     self.assertEqual(result, {'status': 400, 'books_lacking': [{'quantity_purchased': 10}], 'stocks': False})
    #
    #     mock_book.list_rejected_items.append.return_value = None
    #
    #     result = verify_stock([])
    #     self.assertEqual(result, {'books_stocks': [{'format': '', 'item_price': 1, 'item_quantity': 10, 'page_quantity': 1}], 'digital': True, 'status': 200, 'stocks': True, 'total_price': 0.0})
    #
    # @mock.patch("controllers.book_controller.book_db")
    # def test_reserve_books_works(self, mock_book_db):
    #     result = reserve_books([], [])
    #     self.assertEqual(result, "Reserva realizada com sucesso!")
    #
    #
    #     result = reserve_books([], None)
    #     self.assertEqual(result, "Erro: 'NoneType' object is not iterable")
    #
    #     result2 = reserve_books([{"quantity_purchased":10}], [{"item_quantity":20, "reserve_quantity":20}])
    #     self.assertEqual(result2, "Reserva realizada com sucesso!")
    #
    # @mock.patch("controllers.book_controller.book_db")
    # def test_finish_purshase_works(self, mock_book_db):
    #     mock_book_db.search_books_by_id.return_value = [{"item_price":1, "item_quantity":10, "page_quantity":1, "format": ""}]
    #
    #     result = finish_purchase([], True)
    #     self.assertEqual(result, {'status': 400, 'text': 'Erro: reserve_quantity'})
    #
    #     mock_book_db.search_books_by_id.return_value = [{"item_price": 1, "item_quantity": 1, "quantity_purchased": 1, "reserve_quantity":1, "item_quantity":1}]
    #     result = finish_purchase([{"item_quantity":1, "reserve_quantity":1, "quantity_purchased":1}], True)
    #     self.assertEqual(result, {'status': 200, 'text': 'Estoque alterado com sucesso!'})
    #
    #     mock_book_db.search_books_by_id.return_value = [{"item_price": 1, "item_quantity": 1, "quantity_purchased": 1, "reserve_quantity":1, "item_quantity":1}]
    #     result = finish_purchase([{"item_quantity":1, "reserve_quantity":1, "quantity_purchased":1}], False)
    #     self.assertEqual(result, {'status': 200, 'text': 'Estoque alterado com sucesso!'})
    #
    # @mock.patch("controllers.book_controller.book_db")
    # def test_insert_book_validations_works(self, mock_book_db):
    #
    #     with self.assertRaises(Exception) as error:
    #         validate_book(dict(item_price=0))
    #     self.assertEqual("O preço deve ser maior que zero.", error.exception.args[0])
    #
    #     with self.assertRaises(Exception) as error:
    #         validate_book(dict(item_quantity=-1, item_price=1))
    #     self.assertEqual("A quantidade de livros deve ser maior ou igual a zero.", error.exception.args[0])
    #
    #     with self.assertRaises(Exception) as error:
    #         validate_book(dict(item_quantity=0, item_price=1, page_quantity=0))
    #     self.assertEqual("A quantidade de páginas do livro deve ser maior que zero.", error.exception.args[0])
    #
    #     with self.assertRaises(Exception) as error:
    #         validate_book(dict(item_quantity=0, item_price=1, page_quantity=1, format="Físico", weight=0))
    #     self.assertEqual("O peso de um livro físico deve ser maior que zero.", error.exception.args[0])
    #
    #     with self.assertRaises(Exception) as error:
    #         validate_book(dict(item_quantity=0, item_price=1, page_quantity=1, format="Físico", weight=1, size=dict(height=0)))
    #     self.assertEqual("A altura de um livro físico deve ser maior que zero.", error.exception.args[0])
    #
    #     with self.assertRaises(Exception) as error:
    #         validate_book(dict(item_quantity=0, item_price=1, page_quantity=1, format="Físico", weight=1, size=dict(height=1, lenght=0),))
    #     self.assertEqual("O comprimento de um livro físico deve ser maior que zero.", error.exception.args[0])
    #
    #     with self.assertRaises(Exception) as error:
    #         validate_book(dict(item_quantity=0, item_price=1, page_quantity=1, format="Físico", weight=1, size=dict(height=1, lenght=1, width=0)))
    #     self.assertEqual("A largura de um livro físico deve ser maior que zero.", error.exception.args[0])
    #
    #     with self.assertRaises(Exception) as error:
    #         validate_book(dict(item_quantity=0, item_price=1, page_quantity=1, format="Físico", weight=1, size=dict(height=1, lenght=1, width=1), published_at="01/10/2025"))
    #     self.assertEqual("A data de publicação é inválida.", error.exception.args[0])
    #
    #     with self.assertRaises(Exception) as error:
    #         dict_values = dict(item_quantity=0, item_price=1, page_quantity=1, format="Físico", weight=1, size=dict(height=1, lenght=1, width=1), published_at="01/10/2020")
    #         dict_values['isbn-10'] = "111111111"
    #         validate_book(dict_values)
    #     self.assertEqual("Formato inválido!", error.exception.args[0])
    #
    #     with self.assertRaises(Exception) as error:
    #         dict_values = dict(item_quantity=0, item_price=1, page_quantity=1, format="Físico", weight=1, size=dict(height=1, lenght=1, width=1), published_at="01/10/2020")
    #         dict_values['isbn-10'] = "111111111"
    #         dict_values['isbn-13'] = "111111111"
    #         validate_book(dict_values)
    #     self.assertEqual("Formato inválido!", error.exception.args[0])
    #
    #     mock_book_db.isbn_exists_db.return_value = True
    #     with self.assertRaises(Exception) as error:
    #         dict_values = dict(item_quantity=0, item_price=1, page_quantity=1, format="Físico", weight=1, size=dict(height=1, lenght=1, width=1), published_at="01/10/2020")
    #         dict_values['isbn-10'] = "1111111111"
    #         dict_values['isbn-13'] = "1111111111111"
    #         validate_book(dict_values)
    #     self.assertEqual("Isbn 10 já cadastrado.", error.exception.args[0])
    #     mock_book_db.isbn_exists_db.return_value = False
    #
    #     with self.assertRaises(Exception) as error:
    #         dict_values = dict(item_quantity=0, item_price=1, page_quantity=1, format="Físico", weight=1, size=dict(height=1, lenght=1, width=1), published_at="01/10/2020")
    #         dict_values['isbn-10'] = "1111111111"
    #         dict_values['isbn-13'] = "fasdfasdfdsfadsfadsfadsfadfadsf"
    #         validate_book(dict_values)
    #     self.assertEqual("Formato inválido!", error.exception.args[0])
    #
    #     mock_book_db.isbn_exists_db.side_effect = [False, True]
    #     with self.assertRaises(Exception) as error:
    #         dict_values = dict(item_quantity=0, item_price=1, page_quantity=1, format="Físico", weight=1, size=dict(height=1, lenght=1, width=1), published_at="01/10/2020")
    #         dict_values['isbn-10'] = "1111111111"
    #         dict_values['isbn-13'] = "7777777777777"
    #         validate_book(dict_values)
    #     self.assertEqual("Isbn 13 já cadastrado.", error.exception.args[0])
