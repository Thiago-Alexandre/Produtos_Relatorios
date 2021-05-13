from pymongo.errors import CollectionInvalid, PyMongoError

from db import DB


# Returns a country name list or None if nothing is find:
def get_country_name_list() -> list:
    result_data = None

    try:
        country = DB.country

        countries_db = list(country.find({}, {"_id": 0}))

        if len(countries_db) > 0:
            result_data = [c["name"] for c in countries_db]
    except CollectionInvalid as error:
        raise Exception(f"CollectionInvalid error: {error}")
    except PyMongoError as error:
        raise Exception(f"Other PyMongo error: {error}")
    except Exception as error:
        raise Exception(f"Other error ocurred: {error}")

    return result_data


# Returns dict if country exists in database or None if not or throw exception:
def search_country(name_country: str) -> dict or None:

    try:
        country = DB.country

        return country.find_one({"name": name_country}, {"_id": 0})

    except CollectionInvalid as error:
        raise Exception(f"CollectionInvalid error: {error}")
    except PyMongoError as error:
        raise Exception(f"Other PyMongo error: {error}")
    except Exception as error:
        raise Exception(f"Other error ocurred: {error}")
