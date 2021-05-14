# from database import import book_db
from datetime import datetime

def insert_book(dict_values: dict) -> dict:
    try:
        if float(dict_values['item_price']) <= 0:
            return dict(status=400, text="O preço deve ser maior que zero")
        elif float(dict_values['weight']) <= 0:
            return dict(status=400, text="O peso do livro deve ser maior que zero")
        elif float(dict_values['size']['height']) <= 0:
            return dict(status=400, text="A altura do livro deve ser maior que zero")
        elif float(dict_values['size']['lenght']) <= 0:
            return dict(status=400, text="O comprimento do livro deve ser maior que zero")
        elif float(dict_values['size']['width']) <= 0:
            return dict(status=400, text="A largura do livro deve ser maior que zero")
        elif int(dict_values['item_quantity']) < 0:
            return dict(status=400, text="A quantidade de livros deve ser maior ou igual a zero")
        elif int(dict_values['page_quantity']) <= 0:
            return dict(status=400, text="O quantidade da páginas do livro deve ser maior que zero")
        datetime.strptime(dict_values['published_at'], "%Y-%m-%d")
    except Exception as error:
        return dict(status=400, text=f"valor informado inválido.  {error}")

    # if not book_db.isbn_exists_db(dict_values['isbn-10']) and not book_db.isbn_exists_db(dict_values['isbn-13']):
    #     return dict(status=200, text="livro cadastrado com sucesso")


x = insert_book(dict({
    "_id": "",
    "title": "Building Microservices: Designing Fine-Grained Systems",
    "description": "",
    "language": "English",
    "category": [
        "Computação",
        "Informática",
        "Mídias Digitais"
    ],
    "author": [
        {
            "name": "Martin",
            "lastname": "Fowler",
            "country": "United States of America"
        },
        {
            "name": "Thiago",
            "lastname": "Alexandre",
            "country": "Brazil"
        }
    ],
    "edition": 1,
    "publisher": {
        "name": "O'Reilly Media",
        "country": "United States of America"
    },
    "isbn-10": "1491950358",
    "isbn-13": "9781491950357",
    "format": "Fisical",
    "published_at": "2015-02-20",
    "item_price": "a302.01",
    "item_quantity": 928,
    "classification": [
        {
            "author_name": "Carlos Eduardo Ribeiro",
            "comment": "Muito bom...",
            "classification": 5,
            "created_at": "2021-05-11"
        },
        {
            "author_name": "Gabriela Cristofolini",
            "comment": "Excelente didática...",
            "classification": 4,
            "created_at": "2021-05-11"
        },
        {
            "author_name": "Jeff Silva",
            "comment": "Autor explica muito...",
            "classification": 5,
            "created_at": "2021-05-11"
        }
    ],
    "size": {
        "height": 17.78,
        "lenght": 23.54,
        "width": 1.5
    },
    "weight": 1.5,
    "page_quantity": 270
}))

print(x)