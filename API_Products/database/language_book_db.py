from pymongo.errors import CollectionInvalid

from database.db import get_db


# Returns a language name list or None if nothing is find:
def get_language_book_list_db() -> list or None:
    try:
        db = get_db()
        language_book = db.language_book
        result_data = list(language_book.find({}, {"_id": 0}))

        if len(result_data):
            return result_data
    except CollectionInvalid as error:
        raise Exception(f"PyMongo Collection Ivalid error: {error.args[0]}")
    except Exception as error:
        raise Exception(f"Other error: {error.args[0]}")
