from additionals.functions import convert_object_id_to_string
from .db import DB


def insert_publishers_db(dict_values: dict) -> str:
    if dict_values:
        DB["publisher"].insert_one(dict_values)
        return "Registro inserido com sucesso!"
    else:
        raise Exception("Registro inválido.")


def read_all_publishers_db() -> list:
    publishers  = DB.publisher.find()

    publishers_list = convert_object_id_to_string(publishers)
    
    if publishers_list:
        return publishers_list
    else:
        raise Exception("Nenhuma editora encontrada!")


def delete_publishers_db(dict_values: dict) -> str:
    publisher_name = dict_values['name']
    publisher_country = dict_values['country']    

    affected_rows = DB.publisher.delete_one({"name": publisher_name, "country": publisher_country}).deleted_count

    if affected_rows:
        return "Registro excluído com sucesso!"
    else:
        raise Exception("Nenhuma editora encontrada!")