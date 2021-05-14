from .db import DB
from API_Products.additionals.functions import convert_object_id_to_string


def insert_categories_db(dict_values: dict):
    if dict_values:
        DB["category"].insert_one(dict_values)
    else:
        raise Exception("Registro inválido.")


def read_all_categories_db() -> list:
    categories = list(DB["category"].find())
    categories_list = convert_object_id_to_string(categories)
    if categories_list:
        return categories_list
    raise Exception("Nenhuma categoria encontrada.")

