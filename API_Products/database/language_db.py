from pymongo.errors import CollectionInvalid, PyMongoError

from db import DB


# Returns a language name list or None if nothing is find:
def get_language_list() -> list or None:
    try:
        language = DB.language
        result_data = list(language.find({}, {"_id": 0}))
        if len(result_data):
            return result_data
    except CollectionInvalid as error:
        raise Exception(f"CollectionInvalid error: {error}")
    except PyMongoError as error:
        raise Exception(f"Other PyMongo error: {error}")
    except Exception as error:
        raise Exception(f"Other error ocurred: {error}")
