from pymongo.errors import CollectionInvalid, PyMongoError
from additionals.functions import convert_object_id_to_string
from .db import DB


def insert_book_db(dict_values: dict):

    if dict_values:
        DB.book.insert_one(dict_values)
        return "Registrado com sucesso!"
    else:
        raise Exception("Registros inválidos.")


def read_all_books_db() -> list:

    book = DB.book.find()
    book_list = convert_object_id_to_string(book)

    if book_list:
        return book_list
    else:
        raise Exception("Nenhum livro encontrado!")


def isbn_exists_db(isbn_to_check: str) -> bool:
    if not isinstance(isbn_to_check, str):
        return False

    # Grants wheter all isbn characters is numeric:
    isbn = [s for s in list(isbn_to_check) if s.isdigit()]
    isbn = "".join(isbn)

    # Checks if exists a book with provided isbn in db:
    try:
        book = DB.book
        query_result = book.find_one({"$or": [{"isbn-10": isbn}, {"isbn-13": isbn}]})

        return True if query_result else False
    except CollectionInvalid as error:
        raise Exception(f"CollectionInvalid error: {error.args[0]}")
    except PyMongoError as error:
        raise Exception(f"Other PyMongo error: {error.args[0]}")

