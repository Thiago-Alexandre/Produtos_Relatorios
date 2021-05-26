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

    @mock.patch("controllers.book_controller.update_book_db")
    @mock.patch("controllers.book_controller.get_books_by_id")
    def test_check_stock(self, mock_get_books_by_id, mock_update_book_db):
        mock_get_books_by_id.side_effect = Exception("Teste")
        self.assertEqual(check_stock([dict(item_id=""), dict(item_id="")]),
                         dict(status=400, error="Teste", message="Verifique os dados informados."))

        shopping_cart_no_stock = [dict(item_id="", quantity_purchased=15), dict(item_id="", quantity_purchased=15)]
        book_list_db_no_stock = [dict(item_quantity=10, item_price=0.0, format=dict(digital=True)),
                                 dict(item_quantity=10, item_price=0.0, format=dict(digital=True))]

        shopping_cart_stock_ok = [dict(item_id="", quantity_purchased=5), dict(item_id="", quantity_purchased=5)]
        book_list_db_stock_ok = [dict(item_quantity=10, item_price=0.0, format=dict(digital=False), reserve_quantity=0),
                                 dict(item_quantity=10, item_price=0.0, format=dict(digital=False), reserve_quantity=0)]

        mock_get_books_by_id.side_effect = [[], book_list_db_stock_ok, book_list_db_no_stock]
        mock_update_book_db.side_effect = [Exception("Teste"), book_list_db_stock_ok, book_list_db_no_stock]

        self.assertEqual(check_stock([]),
                         dict(status=500, error="Teste", message="Não foi possível reservar produtos do estoque."))

        self.assertEqual(check_stock(shopping_cart_stock_ok),
                         dict(status=200, books_stocks=[{'format': {'digital': False}, 'item_price': 0.0,
                                                         'item_quantity': 5, 'reserve_quantity': 5},
                                                        {'format': {'digital': False}, 'item_price': 0.0,
                                                         'item_quantity': 5, 'reserve_quantity': 5}],
                              stocks=True, total_price=0.0, digital=False, books=[{'format': {'digital': False},
                                                                                   'item_price': 0.0,
                                                                                   'item_quantity': 5,
                                                                                   'reserve_quantity': 5},
                                                                                  {'format': {'digital': False},
                                                                                   'item_price': 0.0,
                                                                                   'item_quantity': 5,
                                                                                   'reserve_quantity': 5}]))

        self.assertEqual(check_stock(shopping_cart_no_stock),
                         dict(status=400, books_lacking=[{'item_id': '', 'quantity_purchased': 10},
                                                         {'item_id': '', 'quantity_purchased': 10}], stocks=False))

    @mock.patch("controllers.book_controller.update_book_db")
    @mock.patch("controllers.book_controller.get_books_by_id")
    def test_finish_purchase(self, mock_get_books_by_id, mock_update_book_db):
        mock_get_books_by_id.side_effect = Exception("Teste")
        self.assertEqual(finish_purchase([dict(item_id=""), dict(item_id="")], True),
                         dict(status=400, error="Teste", message="Verifique os dados informados."))

        shopping_cart_error = [dict(item_id="", quantity_purchased=15), dict(item_id="", quantity_purchased=15)]
        book_list_db_error = [dict(item_quantity=0, item_price=0.0, format=dict(digital=False), reserve_quantity=10),
                              dict(item_quantity=0, item_price=0.0, format=dict(digital=False), reserve_quantity=10)]

        shopping_cart_ok = [dict(item_id="", quantity_purchased=5), dict(item_id="", quantity_purchased=5)]
        book_list_db_ok = [dict(_id="", item_quantity=0, item_price=0.0, format=dict(digital=False),
                                reserve_quantity=5),
                           dict(_id="", item_quantity=0, item_price=0.0, format=dict(digital=False),
                                reserve_quantity=5)]

        mock_get_books_by_id.side_effect = [book_list_db_error, book_list_db_error,
                                            book_list_db_ok, book_list_db_ok, book_list_db_ok, book_list_db_ok]

        self.assertEqual(finish_purchase(shopping_cart_error, True),
                         dict(status=400, error="Erro ao finalizar a compra.",
                              message="A quantidade de livros informada está incorreta."))

        self.assertEqual(finish_purchase(shopping_cart_error, False),
                         dict(status=400, error="Erro ao devolver livros ao estoque.",
                              message="A quantidade de livros informada está incorreta."))

        mock_update_book_db.side_effect = [Exception("Teste"), [], ["teste", "teste"], ["teste", "teste"]]

        self.assertEqual(finish_purchase(shopping_cart_ok, True),
                         dict(status=500, error="Teste", message="Compra não finalizada."))

        self.assertEqual(finish_purchase(shopping_cart_ok, True),
                         dict(status=500, error="Não foi possível atualizar os dados dos livros.",
                              message="Compra não finalizada"))

        self.assertEqual(finish_purchase(shopping_cart_ok, True),
                         dict(status=200, message="Compra finalizada! Estoque alterado com sucesso.",
                              books=['teste', 'teste']))

        self.assertEqual(finish_purchase(shopping_cart_ok, False),
                         dict(status=200, message="Compra não finalizada! Produtos devolvidos ao estoque.",
                              books=['teste', 'teste']))
