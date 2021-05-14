from database.db import DB
from pymongo.errors import CollectionInvalid, PyMongoError


# Returns a book format list or None if nothing is find:
def get_book_format_list_db() -> list or None:
    try:
        book_format = DB.format
        query_result = list(book_format.find({}, {"_id": 0}))

        if len(query_result) > 0:
            return query_result
    except CollectionInvalid as error:
        raise Exception(f"Collection Ivalid error: {error.args[0]}")
    except PyMongoError as error:
        raise Exception(f"Other PyMongo error: {error.args[0]}")
