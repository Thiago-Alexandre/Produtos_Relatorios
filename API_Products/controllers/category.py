from database import category_db
from database.db import get_db


def read_all_categories() -> dict:
    try:
        categories = category_db.read_all_categories_db()
        return dict(status=200, result_data=categories)
    except Exception as error:
        return dict(status=500, error=error.args[0], message="Tente novamente mais tarde.")


def insert_categories(dict_values: dict) -> dict:
    if "name" not in list(dict_values.keys()) or dict_values["name"].strip() == "":
        return dict(status=400, error="Valor inserido inválido.", message="Verifique os dados informados.")

    dict_values["name"] = dict_values["name"].capitalize()

    db = get_db()
    validate_category = db["category"].count_documents(dict_values, {})

    if not validate_category > 0:
        try:
            category_db.insert_categories_db(dict_values)
            return dict(status=200, message="Cadastrado com sucesso.")
        except Exception as error:
            return dict(
                status=400,
                error=f"Categoria não cadastrada: {error}",
                message="Verifique a categoria informada!"
            )
    else:
        return dict(status=400, error="Categoria não cadastrada.", message="A catoria já existe no sistema.")
