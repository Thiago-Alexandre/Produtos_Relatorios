from API_Products.database import category_db
from API_Products.database.db import get_db


def read_all_categories() -> dict:
    try:
        categories = category_db.read_all_categories_db()
        return dict(status=200, result_data=categories)
    except Exception as error:
        return dict(status=500, error="Nenhuma categoria foi encontrada.", message="Tente novamente mais tarde.")


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
                error=f"Categoria não cadastrada: {error}.",
                message="Verifique a categoria informada!"
            )
    else:
        return dict(status=400, error="Categoria não cadastrada.", message="A categoria já existe no sistema.")


def delete_categories(dict_values: dict):
    if "name" not in list(dict_values.keys()) or dict_values["name"].strip() == "":
        return dict(status=400, error="Valor inserido inválido.", message="Verifique os dados informados.")

    dict_values["name"] = dict_values["name"].capitalize()
    db = get_db()
    if db["book"].find_one({"category": dict_values["name"]}):
        return dict(status=400, error="A categoria está sendo utilizada.", message="Não é possível deletá-la.")
    else:
        deleted_count = category_db.delete_categories_db(dict_values)
        if deleted_count:
            return dict(status=200, message="Categoria deletada com sucesso.")
        return dict(status=500, error="Erro interno.", message="A categoria não foi deletada.")


def update_categories(dict_values: dict):
    if "name" not in list(dict_values.keys()) or dict_values["name"].strip() == "":
        return dict(status=400, error="Valor inserido inválido.", message="Verifique os dados informados.")

    dict_values["new_name"] = dict_values["new_name"].capitalize()
    db = get_db()

    if db["category"].find_one({"name": dict_values["new_name"]}):
        return dict(status=400, erro="Já existe uma categoria com este nome.", message="Verifique os dados informados.")

    updated_category = category_db.update_categories_db(dict_values)
    if not updated_category:
        return dict(status=500, error="Erro interno.", message="A categoria não foi modificada.")
    else:
        db["book"].update_many({}, {"$set": {"category.$[element]": dict_values["new_name"]}},
                               array_filters=[{"element": dict_values["old_name"]}])
        return dict(status=200, message="Categoria alterada com sucesso.")
