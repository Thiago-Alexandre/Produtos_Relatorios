from builtins import delattr

from API_Products.controllers.book import *
from unittest import mock, TestCase

class TestBook(TestCase):

    @mock.patch("API_Products.controllers.book")
    @mock.patch("API_Products.controllers.book.book_db")
    def test_insert_book_works(self, mock_book_db, mock_book):
        mock_book.insert_book_validations.return_value = None
        mock_book_db.insert_book_db.return_value = "Success"

        result = insert_book({"item_price":1, "item_quantity":1, "page_quantity":1, "format":"", "published_at":"10/10/2020", "isbn-10":'7987356178', "isbn-13":"1234567876453"})
        self.assertEqual(result, {'status': 200, 'message': 'Livro cadastrado com sucesso!'})

        delattr(mock_book_db, "insert_book_db")
        result = insert_book({"item_price":1, "item_quantity":1, "page_quantity":1, "format":"", "published_at":"10/10/2020", "isbn-10":'7987356178', "isbn-13":"1234567876453"})
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




