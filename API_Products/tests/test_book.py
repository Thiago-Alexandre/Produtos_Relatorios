from builtins import delattr

from API_Products.controllers.book import *
from unittest import mock, TestCase

class TestBook(TestCase):

    @mock.patch("API_Products.controllers.book")
    @mock.patch("API_Products.controllers.book.book_db")
    def test_insert_book_works(self, mock_book_db, mock_book):
        mock_book.insert_book_validations.return_value = None
        mock_book_db.insert_book_db.return_value = "Success"
        mock_book_db.isbn_exists_db.return_value = False

        result = insert_book({"item_price":1, "item_quantity":1, "page_quantity":1, "format":"", "published_at":"10/10/2020", "isbn-10":'4564564565', "isbn-13":"4564564564564"})
        self.assertEqual(result, {'status': 200, 'message': 'Livro cadastrado com sucesso!'})

        delattr(mock_book_db, "insert_book_db")
        result = insert_book({"item_price":1, "item_quantity":1, "page_quantity":1, "format":"", "published_at":"10/10/2020", "isbn-10":'4444444444', "isbn-13":"3333333333333"})
        self.assertEqual(result, {'error': 'insert_book_db', 'message': 'Verifique os dados informados.', 'status': 400})

    @mock.patch("API_Products.controllers.book")
    @mock.patch("API_Products.controllers.book.book_db")
    def test_verify_stock_works(self, mock_book_db, mock_book):
        mock_book_db.search_books_for_id.return_value = [{"item_price":1, "item_quantity":10, "page_quantity":1, "format":""}]

        result = verify_stock([dict(quantity_purchased=20)])
        self.assertEqual(result, {'status': 400, 'books_lacking': [{'quantity_purchased': 10}], 'stocks': False})

        mock_book.list_rejected_items.append.return_value = None

        result = verify_stock([])
        self.assertEqual(result, {'books_stocks': [{'format': '', 'item_price': 1, 'item_quantity': 10, 'page_quantity': 1}], 'digital': True, 'status': 200, 'stocks': True, 'total_price': 0.0})

    def test_reserve_books_works(self):
        result = reserve_books([],[])
        self.assertEqual(result, "Reserva realizada com sucesso!")


        result = reserve_books([], None)
        self.assertEqual(result, "Erro: 'NoneType' object is not iterable")

        result = reserve_books([{"quantity_purchased":10}], [{"item_quantity":20, "reserve_quantity":20}])
        self.assertEqual(result, "")

    @mock.patch("API_Products.controllers.book.book_db")
    def test_finish_purshase_works(self, mock_book_db):
        mock_book_db.search_books_for_id.return_value = [{"item_price":1, "item_quantity":10, "page_quantity":1, "format":""}]

        result = finish_purshase([], True)
        self.assertEqual(result, {'status': 400, 'text': 'Erro: reserve_quantity'})

        mock_book_db.search_books_for_id.return_value = [{"item_price": 1, "item_quantity": 1, "quantity_purchased": 1, "reserve_quantity":1, "item_quantity":1}]
        result = finish_purshase([{"item_quantity":1, "reserve_quantity":1, "quantity_purchased":1}], True)
        self.assertEqual(result, {'status': 200, 'text': 'Estoque alterado com sucesso!'})

        mock_book_db.search_books_for_id.return_value = [{"item_price": 1, "item_quantity": 1, "quantity_purchased": 1, "reserve_quantity":1, "item_quantity":1}]
        result = finish_purshase([{"item_quantity":1, "reserve_quantity":1, "quantity_purchased":1}], False)
        self.assertEqual(result, {'status': 200, 'text': 'Estoque alterado com sucesso!'})

    @mock.patch("API_Products.controllers.book.book_db")
    def test_insert_book_validations_works(self, mock_book_db):

        with self.assertRaises(Exception) as error:
            insert_book_validations(dict(item_price=0))
        self.assertEqual("O preço deve ser maior que zero.", error.exception.args[0])

        with self.assertRaises(Exception) as error:
            insert_book_validations(dict(item_quantity=-1, item_price=1))
        self.assertEqual("A quantidade de livros deve ser maior ou igual a zero.", error.exception.args[0])

        with self.assertRaises(Exception) as error:
            insert_book_validations(dict(item_quantity=0, item_price=1, page_quantity=0))
        self.assertEqual("A quantidade de páginas do livro deve ser maior que zero.", error.exception.args[0])

        with self.assertRaises(Exception) as error:
            insert_book_validations(dict(item_quantity=0, item_price=1, page_quantity=1, format="Físico", weight=0))
        self.assertEqual("O peso de um livro físico deve ser maior que zero.", error.exception.args[0])

        with self.assertRaises(Exception) as error:
            insert_book_validations(dict(item_quantity=0, item_price=1, page_quantity=1, format="Físico", weight=1, size=dict(height=0)))
        self.assertEqual("A altura de um livro físico deve ser maior que zero.", error.exception.args[0])

        with self.assertRaises(Exception) as error:
            insert_book_validations(dict(item_quantity=0, item_price=1, page_quantity=1, format="Físico", weight=1, size=dict(height=1, lenght=0),))
        self.assertEqual("O comprimento de um livro físico deve ser maior que zero.", error.exception.args[0])

        with self.assertRaises(Exception) as error:
            insert_book_validations(dict(item_quantity=0, item_price=1, page_quantity=1, format="Físico", weight=1, size=dict(height=1, lenght=1, width=0)))
        self.assertEqual("A largura de um livro físico deve ser maior que zero.", error.exception.args[0])

        with self.assertRaises(Exception) as error:
            insert_book_validations(dict(item_quantity=0, item_price=1, page_quantity=1, format="Físico", weight=1, size=dict(height=1, lenght=1, width=1), published_at="01/10/2025"))
        self.assertEqual("A data de publicação é inválida.", error.exception.args[0])

        with self.assertRaises(Exception) as error:
            dict_values = dict(item_quantity=0, item_price=1, page_quantity=1, format="Físico", weight=1, size=dict(height=1, lenght=1, width=1), published_at="01/10/2020")
            dict_values['isbn-10'] = "111111111"
            insert_book_validations(dict_values)
        self.assertEqual("Formato inválido!", error.exception.args[0])

        with self.assertRaises(Exception) as error:
            dict_values = dict(item_quantity=0, item_price=1, page_quantity=1, format="Físico", weight=1, size=dict(height=1, lenght=1, width=1), published_at="01/10/2020")
            dict_values['isbn-10'] = "111111111"
            dict_values['isbn-13'] = "111111111"
            insert_book_validations(dict_values)
        self.assertEqual("Formato inválido!", error.exception.args[0])

        mock_book_db.isbn_exists_db.return_value = True
        with self.assertRaises(Exception) as error:
            dict_values = dict(item_quantity=0, item_price=1, page_quantity=1, format="Físico", weight=1, size=dict(height=1, lenght=1, width=1), published_at="01/10/2020")
            dict_values['isbn-10'] = "1111111111"
            dict_values['isbn-13'] = "1111111111111"
            insert_book_validations(dict_values)
        self.assertEqual("Isbn 10 já cadastrado.", error.exception.args[0])
        mock_book_db.isbn_exists_db.return_value = False

        with self.assertRaises(Exception) as error:
            dict_values = dict(item_quantity=0, item_price=1, page_quantity=1, format="Físico", weight=1, size=dict(height=1, lenght=1, width=1), published_at="01/10/2020")
            dict_values['isbn-10'] = "1111111111"
            dict_values['isbn-13'] = "fasdfasdfdsfadsfadsfadsfadfadsf"
            insert_book_validations(dict_values)
        self.assertEqual("Formato inválido!", error.exception.args[0])

        mock_book_db.isbn_exists_db.side_effect = [False, True]
        with self.assertRaises(Exception) as error:
            dict_values = dict(item_quantity=0, item_price=1, page_quantity=1, format="Físico", weight=1, size=dict(height=1, lenght=1, width=1), published_at="01/10/2020")
            dict_values['isbn-10'] = "1111111111"
            dict_values['isbn-13'] = "7777777777777"
            insert_book_validations(dict_values)
        self.assertEqual("Isbn 13 já cadastrado.", error.exception.args[0])




