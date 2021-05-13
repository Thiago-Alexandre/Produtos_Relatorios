from requests import get
from requests.exceptions import HTTPError
from database.db import DB
from pymongo.errors import CollectionInvalid

__API_URL = "https://restcountries.eu/rest/v2/all"
__PARAMS = dict(fields="translations")


# This function requests a list of country names to an API and save this names in DB:
def populate_countries():
    countries = list()

    # Requests the list of country names to API and save it:
    try:
        request_response = get(__API_URL, params=__PARAMS)
        response_data = request_response.json()

        for country in response_data:
            countries.append(dict(name=country["translations"]["br"]))
    except HTTPError as http_error:
        print(f"HTTP error ocurred: {http_error}")
    except Exception as error:
        print(f"Other error ocurred: {error}")

    # Save the list in the db:
    try:
        country = DB.country
        country.insert_many(countries)
    except CollectionInvalid as error:
        print(f"PyMongo error: {error}")
    except Exception as error:
        print(f"Other error ocurred: {error}")
