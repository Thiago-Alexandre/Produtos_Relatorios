from additionals.functions import convert_object_id_to_string
from database.db import get_db


def insert_author_db(dict_values: dict):
    db = get_db()
    if dict_values:
        db.author.insert_one(dict_values)
        return "Registrado com sucesso!"
    else:
        raise Exception("Registros inválidos.")


def read_all_authors_db() -> list:
    db = get_db()
    author = db.author.find()
    author_list = convert_object_id_to_string(author)

    if author_list:
        return author_list
    else:
        raise Exception("Nenhum autor encontrado!")
