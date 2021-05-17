from database import category_db
from database.db import get_db


def read_all_categories() -> dict:
    try:
        categories = category_db.read_all_categories_db()
        return dict(status=200, text=categories)
    except Exception as error:
        return dict(status=400, text=error.args[0])


def insert_categories(dict_values: dict) -> dict:
    if dict_values["name"].strip() == "":
        return dict(status=400, text="Valor inválido.")

    dict_values["name"] = dict_values["name"].capitalize()

    db = get_db()
    validate_category = db["category"].count_documents(dict_values, {})

    if not validate_category > 0:
        try:
            category_db.insert_categories_db(dict_values)
            return dict(status=200, text="Cadastrado com sucesso.")
        except Exception as error:
            return dict(status=400, text=f"Não foi possível cadastrar a categoria.{error}")

    else:
        return dict(status=400, text="Categoria já cadastrada.")


def delete_categories(dict_values: dict):
    if dict_values["name"].strip() == "":
        return dict(status=400, text="Valor inválido.")
    dict_values["name"] = dict_values["name"].capitalize()
    db = get_db()
    if db["book"].find_one({"category": dict_values["name"]}):
        return dict(status=400, text="A categoria está sendo utilizada, não é possível deletá-la.")
    else:
        deleted_count = category_db.delete_categories_db(dict_values)
        if deleted_count:
            return dict(status=200, text="Categoria deletada com sucesso.")
        return dict(status=500, text="Não foi possível deletar a categoria.")