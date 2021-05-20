from bson.objectid import ObjectId
from pymongo.errors import CollectionInvalid, PyMongoError, InvalidId

from additionals.functions import convert_object_id_to_string
from database.db import get_db


def insert_book_db(dict_values: dict):
    db = get_db()
    if dict_values:
        db.book.insert_one(dict_values)
        return "Registrado com sucesso!"
    else:
        raise Exception("Erro ao cadastrar livro.", "Verifique os valores informados")


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


def search_books_by_id(*args) -> list:

    db = get_db()
    book = db.book

    object_id_list = []
    try:
        object_id_list = [{"_id": ObjectId(str(book_id))} for book_id in args]
    except InvalidId as err:
        raise Exception(f"Erro: {err}")

    query_result = book.find({"$or": object_id_list})
    book_list = convert_object_id_to_string(query_result)

    if book_list:
        return book_list
    else:
        raise Exception("Nenhum livro encontrado!")


def update_book_db(dict_values):
    db = get_db()

    id = dict_values["_id"]
    del dict_values["_id"]

    affected_rows = db.book.update_one({"_id": ObjectId(id)}, {"$set": dict_values}).matched_count

    if affected_rows:
         return "Registro alterado com sucesso!"
    else:
        raise Exception("Nenhum livro encontrado!")


def update_all_publishers_book_db(publishers_field: str, new_value: str):
    db = get_db()

    affected_rows = db.book.update_many({'publisher.name': { '$in':[publishers_field]}}, {'$set':{'publisher.name': new_value}}).matched_count

    if affected_rows:
        return "Registros alterados com sucesso!"
    else:
        raise Exception("Nenhuma editora encontrada!")
