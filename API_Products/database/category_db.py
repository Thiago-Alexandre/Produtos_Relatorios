from db import DB


def insert(dict_values: dict):
    if dict_values:
        DB["category"].insert_one(dict_values)
    else:
        raise Exception("Registro inválido.")


def read_all():
    categorys = list(DB["category"].find())
    if categorys:
        return categorys
    else:
        raise Exception("Nenhuma categoria encontrada.")

