from additionals.functions import convert_object_id_to_string
from database.db import get_db


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

        
def delete_publishers_db(dict_values: dict) -> str:
    publisher_name = dict_values['name']
    publisher_country = dict_values['country']    

    db = get_db()
    affected_rows = db.publisher.delete_one({"name": publisher_name, "country": publisher_country}).deleted_count

    if affected_rows:
        return "Registro excluído com sucesso!"
    else:
        raise Exception("Nenhuma editora encontrada!")


def exists_publisher(dict_values) -> bool:
    db = get_db()    
    
    if db.book.find_one({"publisher.name": dict_values["name"]}):
        return True
    else:
        return False
