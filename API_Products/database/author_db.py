from db import DB


def insert_author_db(dict_values: dict):

    if dict_values:
        DB.author.insert_one(dict_values)
    else:
        raise Exception("Registros inválidos.")


def read_all_authors_db() -> list:

    authors = list(DB.author.find())
    if authors:
        return authors
    else:
        raise Exception("Nenhum autor encontrado.")
