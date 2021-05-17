from pymongo import MongoClient
from pymongo.errors import ConfigurationError, PyMongoError

from auth import *

__DB_CONN = f"mongodb+srv://{DB_USER}:{DB_PASSWD}@{DB_HOST}"


def get_db():
    try:
        __CONN = MongoClient(__DB_CONN, ssl=True, ssl_cert_reqs='CERT_NONE')
        return __CONN[DB_NAME]
    except ConfigurationError as error:
        raise Exception("PyMongo configuration error: " + error.args[0])
    except PyMongoError as error:
        raise Exception("Other PyMongo error: " + error.args[0])
    except Exception as error:
        raise Exception("Other error: " + error.args[0])
