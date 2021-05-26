from additionals.functions import convert_object_id_to_string
from database.db import get_db
from bson.objectid import ObjectId


def insert_author_db(dict_values: dict):
    try:
        db = get_db()
        db.author.insert_one(dict_values)
        return "Autor salvo com sucesso!"
    except Exception:
        raise Exception("Ocorreu um erro ao salvar o autor.")


def read_all_authors_db() -> list:
    db = get_db()
    author = db.author.find()
    author_list = convert_object_id_to_string(author)
    if author_list:
        return author_list
    else:
        raise Exception("Nenhum autor encontrado!")


def delete_authors_db(dict_values: dict) -> str:
    try:
        db = get_db()
        db.author.delete_one({"name": dict_values['name'], "lastname": dict_values['lastname'],
                              "country": dict_values['country']})
        return "Registro excluído com sucesso!"
    except Exception:
        raise Exception("Nenhum autor encontrado!")


def update_author_db(dict_values: dict) -> str:
    try:
        db = get_db()
        id_author = ObjectId(dict_values["_id"])
        del dict_values["_id"]
        db.author.update_one({"_id": id_author}, {"$set": dict_values})
        return "Autor alterado com sucesso!"
    except Exception:
        raise Exception("Ocorreu um erro ao alterar o autor!")


def exists_author(dict_values) -> bool:
    db = get_db()
    if db.book.find_one({"author.name": dict_values["name"], "author.lastname": dict_values["lastname"],
                         "author.country": dict_values["country"]}):
        return True
    return False


def validate_author(dict_values) -> bool:
    db = get_db()
    validate = db.author.count_documents(dict_values, {})
    if validate > 0:
        return True
    return False


def search_author(id_author: str) -> dict:
    db = get_db()
    author_saved = db.author.find_one({"_id": ObjectId(id_author)})
    author_saved["_id"] = str(author_saved["_id"])

    if author_saved:
        return author_saved
    raise Exception("Nenhum autor encontrado!")
