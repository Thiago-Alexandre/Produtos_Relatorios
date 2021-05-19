from additionals.functions import convert_object_id_to_string
from database.db import get_db


def insert_author_db(dict_values: dict):
    db = get_db()
    if dict_values:
        db.author.insert_one(dict_values)
        return "Registrado com sucesso!"
    else:
        raise Exception("Registros inválidos.")


def read_all_authors_db() -> list:
    db = get_db()
    author = db.author.find()
    author_list = convert_object_id_to_string(author)

    if author_list:
        return author_list
    else:
        raise Exception("Nenhum autor encontrado!")


def delete_authors_db(dict_values: dict) -> str:
    author_name = dict_values['name']
    author_lastname = dict_values['lastname']
    author_country = dict_values['country']

    db = get_db()
    affected_rows = db.author.delete_one({"name": author_name, "lastname": author_lastname, "country": author_country}).deleted_count

    if affected_rows:
        return "Registro excluído com sucesso!"
    else:
        raise Exception("Nenhum autor encontrado!")


def exist_author(dict_values) -> bool:
    db = get_db()

    if db.book.find_one({"author.name": dict_values["name"], "author.lastname": dict_values["lastname"],
                         "author.country": dict_values["country"]}):
        return True
    else:
        return False
