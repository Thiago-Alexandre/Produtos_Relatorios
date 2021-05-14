from pymongo.errors import CollectionInvalid, PyMongoError
# from additionals.functions import convert_object_id_to_string
from API_Products.database.db import get_db


def insert_book_db(dict_values: dict):
    db = get_db()
    if dict_values:
        db.book.insert_one(dict_values)
        return "Registrado com sucesso!"
    else:
        raise Exception("Registros inválidos.")


def read_all_books_db() -> list:
    db = get_db()
    book = db.book.find()
    book_list = convert_object_id_to_string(book)

    if book_list:
        return book_list
    else:
        raise Exception("Nenhum livro encontrado!")


def isbn_exists_db(isbn_to_check: str) -> bool:

    # Checks if exists a book with provided isbn in db:
    try:
        db = get_db()
        book = db.book
        query_result = book.find_one({"$or": [{"isbn-10": isbn_to_check}, {"isbn-13": isbn_to_check}]})

        return True if query_result else False
    except CollectionInvalid as error:
        raise Exception(f"CollectionInvalid error: {error.args[0]}")
    except PyMongoError as error:
        raise Exception(f"Other PyMongo error: {error.args[0]}")


def check_stock_controller(list_values):
    for dict_values in list_values:
        check_stock_db(dict_values)


def check_stock_db(dict_values):
    db = get_db()
    db.book.find(dict_values, {})



x = [dict(title="TDD com Python: Siga o Bode dos Testes: Usando Django, Selenium e JavaScript", qtd_product=3)]
check_stock_controller(x)
