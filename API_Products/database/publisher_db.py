from additionals.functions import convert_object_id_to_string
from db import get_db


def insert_publishers_db(dict_values: dict) -> str:
    db = get_db()
    if dict_values:
        db.publisher.insert_one(dict_values)
        return "Registro inserido com sucesso!"
    else:
        raise Exception("Registro inválido.")


def read_all_publishers_db() -> list:
    db = get_db()
    publishers = db.publisher.find()

    publishers_list = convert_object_id_to_string(publishers)

    if publishers_list:
        return publishers_list
    else:
        raise Exception("Nenhuma editora encontrada!")
