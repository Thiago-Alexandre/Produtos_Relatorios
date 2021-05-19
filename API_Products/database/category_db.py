from additionals.functions import convert_object_id_to_string
from database.db import get_db


def insert_categories_db(dict_values: dict):
    if dict_values:
        db = get_db()
        db["category"].insert_one(dict_values)
    else:
        raise Exception("Registro inválido.")


def read_all_categories_db() -> list:
    db = get_db()
    categories = list(db["category"].find())
    categories_list = convert_object_id_to_string(categories)
    if categories_list:
        return categories_list
    raise Exception("Nenhuma categoria encontrada.")


def delete_categories_db(dict_values: dict):
    if dict_values:
        db = get_db()
        deleted = db["category"].delete_one(dict_values)
        return deleted.deleted_count
    else:
        raise Exception("Solicitação inválida.")


def update_categories_db(dict_values: dict):
    db = get_db()
    affected_rows = db["category"].update_one({"name": dict_values["old_name"]},
                                              {"$set": {"name": dict_values["new_name"]}}).matched_count

    if affected_rows:
        return "Categoria alterada com sucesso"
    else:
        raise Exception("Nenhuma categoria encontrada.")


