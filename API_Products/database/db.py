from pymongo import MongoClient, errors
from auth import *


__DB_CONN = f"mongodb+srv://{DB_USER}:{DB_PASSWD}@{DB_HOST}"

try:
    __CONN = MongoClient(__DB_CONN, ssl=True, ssl_cert_reqs='CERT_NONE')
    DB = __CONN[DB_NAME]
except errors.PyMongoError as error:
    raise error
