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
        print(f"CollectionInvalid error: {error}")
    except PyMongoError as error:
        print(f"Other PyMongo error: {error}")
    except Exception as error:
        print(f"Other error ocurred: {error}")

    return result_data
