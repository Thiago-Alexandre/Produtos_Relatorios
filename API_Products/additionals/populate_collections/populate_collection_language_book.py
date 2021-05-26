from pymongo.errors import CollectionInvalid

from database.db import get_db


def populate_languages():
    language_list = list()

    # Read a file with the list of language names and save it in db:
    with open("./languages.txt", "r") as languages:
        for lang in languages:
            language_list.append(dict(name=lang.strip()))

    # Save the list in the db:
    try:
        db = get_db()
        language_book = db.language_book
        language_book.delete_many({})
        language_book.insert_many(language_list)
    except CollectionInvalid as error:
        print(f"PyMongo error: {error}")
    except Exception as error:
        print(f"Other error ocurred: {error}")
