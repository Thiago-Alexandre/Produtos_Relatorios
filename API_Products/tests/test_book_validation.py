from unittest import mock, TestCase
from controllers.utils import checks_dict_keys, validate_book, read_all_authors_db, read_all_publishers_db, \
    read_all_categories_db


class TestBookValidation(TestCase):

    def test_checks_dict_keys(self):
        expected = {"title", "description"}
        received = {"title", "description"}

        self.assertEqual(checks_dict_keys(expected, received, "", ""), None)

        received = {"title", "testes"}
        with self.assertRaises(Exception):
            checks_dict_keys(expected, received, "", "")

    @mock.patch("controllers.utils.checks_dict_keys")
    @mock.patch("controllers.utils.get_book_format_list_db")
    @mock.patch("controllers.utils.read_all_categories_db")
    @mock.patch("controllers.utils.read_all_publishers_db")
    @mock.patch("controllers.utils.get_language_book_list_db")
    @mock.patch("controllers.utils.read_all_authors_db")
    def test_validate_book(self, mock_read_all_authors_db, mock_get_language_book_list_db, mock_read_all_publishers_db,
                           mock_read_all_categories_db, mock_get_book_format_list_db, mock_checks_dict_keys):
        book = {
            "title": "Mussum Ipsum, cacilds vidis litro abertis.",
            "description": "Mais vale um bebadis conhecidiss, que um alcoolatra anonimis.",
            "language_book": "Português",
            "category": [
                "Clássicos"
            ],
            "author": [],
            "edition": 1,
            "publisher": {
                "name": "Novatec",
                "country": "Brasil"
            },
            "isbn-10": "6666666666",
            "isbn-13": "9999999999999",
            "format": {
                "name": "Físico",
                "digital": False
            },
            "published_at": "2021-01-01",
            "item_price": 99.99,
            "item_cost_price": 66.66,
            "item_quantity": 666,
            "size": {
                "height": 22.8,
                "lenght": 15.8,
                "width": 3
            },
            "weight": 2,
            "page_quantity": 666
        }

        mock_read_all_authors_db.return_value = [
            {
                '_id': '',
                'name': 'Mussum',
                'lastname': 'Cacilds',
                'country': 'Brasil'
            }
        ]
        mock_get_language_book_list_db.return_value = [{'name': 'Português'}]
        mock_read_all_publishers_db.return_value = [
            {
                '_id': '',
                'name': 'Novatec',
                'country': 'Brasil'
            }
        ]
        mock_read_all_categories_db.return_value = [{'_id': '', 'name': 'Clássicos'}]
        mock_get_book_format_list_db.return_value = [{'name': 'Físico', 'digital': False}]
        mock_checks_dict_keys.return_value = None

        book = dict()

        with self.assertRaises(Exception) as err:
            validate_book(book)
        self.assertEqual(("Invalid body request.", "Dados do autor devem ser uma lista de dicionários."),
                         err.exception.args)


