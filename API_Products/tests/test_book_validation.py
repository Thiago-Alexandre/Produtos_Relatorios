from unittest import mock, TestCase
from controllers.utils import checks_dict_keys


class TestBookValidation(TestCase):

    def test_checks_dict_keys(self):
        expected = {"title", "description"}
        received = {"title", "tests"}

        self.assertEqual(checks_dict_keys(expected, received, "", ""), None)

    @mock.patch("controllers.utils.checks_dict_keys")
    def test_validate_book(self):
        book = {
            "title": "Mussum Ipsum, cacilds vidis litro abertis.",
            "description": "Mais vale um bebadis conhecidiss, que um alcoolatra anonimis.",
            "language_book": "Português",
            "category": [
                "Clássicos"
            ],
            "author": [
                {
                    "name": "Machado de",
                    "lastname": "Assis",
                    "country": "Brasil"
                }
            ],
            "edition": 1,
            "publisher": {
                "name": "Panda Books",
                "country": "Brasil"
            },
            "isbn-10": "8578887239",
            "isbn-13": "9788578887230",
            "format": {
                "name": "Físico",
                "digital": False
            },
            "published_at": "2019-05-03",
            "item_price": 33.94,
            "item_cost_price": 11.50,
            "item_quantity": 100,
            "size": {
                "height": 22.8,
                "lenght": 15.8,
                "width": 3.2
            },
            "weight": 2,
            "page_quantity": 368
        }


