from pymongo import MongoClient
from pymongo.errors import ConfigurationError, PyMongoError

from .auth import *

__DB_CONN = f"mongodb+srv://{DB_USER_NEW_CLUSTER}:{DB_PASSWD_NEW_CLUSTER}@{DB_HOST_NEW_CLUSTER}"
# __DB_CONN = f"mongodb+srv://{DB_USER}:{DB_PASSWD}@{DB_HOST}"


def get_conn():
    try:
        return MongoClient(__DB_CONN)
    except ConfigurationError as error:
        raise Exception("PyMongo configuration error: " + error.args[0])
    except PyMongoError as error:
        raise Exception("Other PyMongo error: " + error.args[0])
    except Exception as error:
        raise Exception("Other error: " + error.args[0])


def get_db():
    try:
        __CONN = get_conn()
        return __CONN[DB_NAME]
    except PyMongoError as error:
        raise Exception("PyMongo error: " + error.args[0])
    except Exception as error:
        raise Exception(error.args[0])
