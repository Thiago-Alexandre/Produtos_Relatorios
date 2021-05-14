from pymongo.errors import CollectionInvalid

from database.db import get_db


# Returns a book format list or None if nothing is find:
def get_book_format_list_db() -> list or None:
    try:
        db = get_db()
        book_format = db.format
        result_data = list(book_format.find({}, {"_id": 0}))

        if len(result_data) > 0:
            return result_data
    except CollectionInvalid as error:
        raise Exception(f"PyMongo Collection Ivalid error: {error.args[0]}")
    except Exception as error:
        raise Exception(error.args[0])
