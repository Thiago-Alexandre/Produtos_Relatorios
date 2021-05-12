from db import DB


def insert_author(dict_values: dict):

    if dict_values:
        DB.author.insert_one(dict_values)
    else:
        raise Exception("Registros inválidos")


def read_all() -> list:

    authors = list(DB.author.find())
    if authors:
        return authors
    else:
        raise Exception("nenhum autor encontrado")
