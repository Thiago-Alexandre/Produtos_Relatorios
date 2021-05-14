from pymongo.errors import CollectionInvalid, PyMongoError

from db import DB


# Returns a language name list or None if nothing is find:
def get_language_book_list() -> list or None:
    try:
        language_book = DB.language_book
        result_data = list(language_book.find({}, {"_id": 0}))
        if len(result_data):
            return result_data
    except CollectionInvalid as error:
        raise Exception(f"CollectionInvalid error: {error}")
    except PyMongoError as error:
        raise Exception(f"Other PyMongo error: {error}")
    except Exception as error:
        raise Exception(f"Other error ocurred: {error}")
