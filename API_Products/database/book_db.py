from bson.objectid import ObjectId
from pymongo import ReturnDocument
from pymongo.errors import CollectionInvalid, PyMongoError, InvalidId

from additionals.functions import convert_object_id_to_string
from database.db import get_db, get_conn


def insert_book_db(dict_values: dict) -> dict or None:
    db = get_db()

    try:
        inserted_id = db["book"].insert_one(dict_values).inserted_id
        if inserted_id:
            return db.book.find_one({"_id": inserted_id})
    except PyMongoError as err:
        raise Exception(f"PyMongo Error: {err.args[0]}", "Erro ao salvar livro no banco de dados.")
    except Exception as err:
        raise Exception(f"Other error: {err.args[0]}", "Erro ao salvar livro no banco de dados.")


def update_book_db(book_values: dict) -> dict or None:
    """
    This function get a book in a dictionary, update your values and returns the book before updating, or none if the
    update fail.
    :param book_values: the book in a dictionary.
    :return:            the book before updating, or none if the update fail.
    """

    db = get_db()

    _id = book_values["_id"]
    del book_values["_id"]

    try:
        before_document = db.book.find_one_and_update(
            filter={"_id": ObjectId(_id)},
            update={"$set": book_values},
            upsert=False,
            return_document=ReturnDocument.BEFORE,
            projection={key: 1 for key in list(book_values.keys())}
        )
        return before_document
    except PyMongoError as err:
        raise Exception(f"PyMongo Error: {err.args[0]}")
    except Exception as err:
        raise Exception(f"Other error: {err.args[0]}")


def update_book_list_db(book_list: list) -> list or None:
    """
    This function get a book list, update your elements and returns other list of books before updating, or None if all
    elements are not updated.
    :param book_list:   a list of books.
    :return:            a list of books before updating, or None if all elements are not updated.
    """

    client = get_conn()
    db = get_db()

    book_list_with_updated_velues = []

    try:
        with client.start_session() as session:
            with session.start_transaction():
                for book in book_list:

                    _id = book["_id"]
                    del book["_id"]

                    before_document = db.book.find_one_and_update(
                        filter={"_id": ObjectId(_id)},
                        update={"$set": book},
                        upsert=False,
                        return_document=ReturnDocument.BEFORE,
                        projection={key: 1 for key in list(book.keys())}
                    )
                    if before_document:
                        book_list_with_updated_velues.append(before_document)
                    else:
                        session.abort_transaction()
                        break

        if len(book_list_with_updated_velues) == len(book_list):
            return book_list_with_updated_velues
    except PyMongoError as err:
        raise Exception(f"PyMongo Error: {err.args[0]}")
    except Exception as err:
        raise Exception(f"Other error: {err.args[0]}")


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


def update_all_publishers_book_db(old_publisher: dict, new_publisher: dict) -> str:
    try:
        db = get_db()
        db.book.update_many({'publisher.name': old_publisher["name"], 'publisher.country': old_publisher["country"]},
                            {'$set': {"publisher.name": new_publisher["name"],
                                      "publisher.country": new_publisher["country"]}})
        return "Registros alterados com sucesso!"
    except Exception:
        raise Exception("Erro ao atualizar os dados dos livros!")


def update_all_authors_book_db(old_author: dict, new_author: dict) -> str:
    try:
        del old_author["_id"]
        db = get_db()
        db.book.update_many({}, {"$set": {"author.$[element]": new_author}},
                            array_filters=[{"element": old_author}])
        return "Registros alterados com sucesso!"
    except Exception as error:
        print(error)
        raise Exception("Erro ao atualizar os dados dos livros!")

