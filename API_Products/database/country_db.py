from pymongo.errors import CollectionInvalid, PyMongoError
import re
from .db import DB


# Returns a country name list or None if nothing is find:
def get_country_name_list_db() -> list or None:
    try:
        country = DB.country

        result_data = list(country.find({}, {"_id": 0}))
        if len(result_data) > 0:
            return result_data
    except CollectionInvalid as error:
        raise Exception(f"CollectionInvalid error: {error}")
    except PyMongoError as error:
        raise Exception(f"Other PyMongo error: {error}")
    except Exception as error:
        raise Exception(f"Other error ocurred: {error}")


# Returns dict if country exists in database or None if not or throw exception:
def search_country(name_country: str) -> dict or None:

    try:
        country = DB.country
        regx = re.compile(f"^{name_country}", re.IGNORECASE)
        return country.find_one({"name": regx}, {"_id": 0})

    except CollectionInvalid as error:
        raise Exception(f"CollectionInvalid error: {error}")
    except PyMongoError as error:
        raise Exception(f"Other PyMongo error: {error}")
    except Exception as error:
        raise Exception(f"Other error ocurred: {error}")
