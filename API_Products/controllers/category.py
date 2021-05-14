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
