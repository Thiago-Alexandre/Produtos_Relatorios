from json import load

from pymongo.errors import CollectionInvalid, PyMongoError

from database.db import DB


def populate_book():
    book_list = []

    with open("books.json") as json_file_books:
        book_list = load(json_file_books)

    try:
        # book = DB.book
        book = DB["book"]
        book.delete_many({})
        book.insert_many(book_list)
    except CollectionInvalid as error:
        print(f"Collection Invalid error: {error.args[0]}")
    except PyMongoError as error:
        print(f"Other PyMongo error: {error.args[0]}")
    except FileExistsError as error:
        print(f"Other error: {error.args[0]}")
