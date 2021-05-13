from database.db import DB
from pymongo.errors import CollectionInvalid


def populate_languages():
    language_list = list()

    # Read a file with the list of language names and save it in db:
    with open("./languages.txt", "r") as languages:
        for lang in languages:
            language_list.append(dict(name=lang.strip()))

    # Save the list in the db:
    try:
        language = DB.language
        language.insert_many(language_list)
    except CollectionInvalid as error:
        print(f"PyMongo error: {error}")
    except Exception as error:
        print(f"Other error ocurred: {error}")
