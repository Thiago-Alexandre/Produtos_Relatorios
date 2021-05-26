from pymongo.errors import CollectionInvalid

from database.db import get_db

__formats = [
    {"name": "Físico", "digital": False},
    {"name": "Braille", "digital": False},
    {"name": "eBook", "digital": True},
    {"name": "audioBook", "digital": True}
]


def populate_format():
    # Save the list in the db:
    try:
        db = get_db()
        book_format = db.format
        book_format.delete_many({})
        book_format.insert_many(__formats)
    except CollectionInvalid as error:
        print(f"PyMongo error: {error}")
    except Exception as error:
        print(f"Other error ocurred: {error}")
