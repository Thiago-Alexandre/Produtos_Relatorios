from pymongo.errors import CollectionInvalid, PyMongoError

from database.db import get_db


def insert_log_db(log_info: dict) -> str:
    try:
        db = get_db()
        log_book = db["log_book"]

        result_data = log_book.insert_one(log_info)

        return str(result_data.inserted_id)
    except CollectionInvalid as error:
        raise Exception(f"CollectionInvalid error: {error}")
    except PyMongoError as error:
        raise Exception(f"Other PyMongo error: {error}")
    except Exception as error:
        raise Exception(f"Other error ocurred: {error}")
