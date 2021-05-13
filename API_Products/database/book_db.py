from database.db import DB
from pymongo.errors import CollectionInvalid, PyMongoError


def isbn_exists(isbn_to_check: str) -> bool:
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
