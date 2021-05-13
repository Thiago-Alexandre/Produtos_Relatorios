from additionals.functions import convert_object_id_to_string
from .db import DB


def insert_author(dict_values: dict):

    if dict_values:
        DB.author.insert_one(dict_values)
        return "Registrado com sucesso!"
    else:
        raise Exception("Registros inválidos.")


def read_all() -> list:

    author = DB.author.find()
    author_list = convert_object_id_to_string(author)

    if author_list:
        return author_list
    else:
        raise Exception("Nenhum autor encontrado!")
