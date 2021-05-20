from additionals.functions import convert_object_id_to_string
from bson.objectid import ObjectId
from database.db import get_db


def insert_publishers_db(dict_values: dict) -> str:
    try:
        db = get_db()
        db.publisher.insert_one(dict_values)
        return "Editora salva com sucesso!"
    except Exception:
        raise Exception("Ocorreu um erro ao salvar a editora.")


def read_all_publishers_db() -> list:
    db = get_db()
    publishers = db.publisher.find()
    publishers_list = convert_object_id_to_string(publishers)
    if publishers_list:
        return publishers_list
    raise Exception("Nenhuma editora encontrada!")

        
def delete_publishers_db(dict_values: dict) -> str:
    db = get_db()
    affected_rows = db.publisher.delete_one({"name": dict_values['name'],
                                             "country": dict_values['country']}).deleted_count
    if affected_rows:
        return "Editora excluída com sucesso!"
    raise Exception("Nenhuma editora encontrada!")


def update_publisher_db(dict_values: dict) -> str:
    db = get_db()
    id_publisher = ObjectId(dict_values["_id"])
    del dict_values["_id"]
    affected_rows = db.publisher.update_one({"_id": id_publisher}, {"$set", dict_values}).matched_count
    if affected_rows:
        return "Editora alterada com sucesso!"
    raise Exception("Nenhuma editora encontrada!")

    
def exists_publisher(dict_values) -> bool:
    db = get_db()
    if db.book.find_one({"publisher.name": dict_values["name"], "publisher.country": dict_values["country"]}):
        return True
    else:
        return False


def validate_publisher(dict_values) -> bool:
    db = get_db()
    validate = db.publisher.count_documents(dict_values, {})
    if validate > 0:
        return True
    else:
        return False


def search_publisher(id_publisher: str) -> dict:
    db = get_db()
    publisher = db.publisher
    publisher_saved = publisher.find_one({"_id": ObjectId(id_publisher)})
    publisher_saved["_id"] = str(publisher_saved["_id"])

    if publisher_saved:
        return publisher_saved
    else:
        raise Exception("Nenhuma editora encontrada!")
