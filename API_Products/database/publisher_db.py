from additionals.functions import convert_object_to_str
from .db import DB


def insert(dict_values: dict) -> str:
    if dict_values:
        DB["publisher"].insert_one(dict_values)#.inserted_id
        return "Registro inserido com sucesso !"
    else:
        raise Exception("Registro inválido.")


def read_all() -> list:
    publishers  = DB.publisher.find()  
    publishers_list = convert_object_id_to_string(publishers)
    
    if publishers_list:
        return publishers_list
    else:
        raise Exception ("Nenhuma editora encontrada !")      

