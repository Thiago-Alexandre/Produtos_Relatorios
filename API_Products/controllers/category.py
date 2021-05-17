from API_Products.database import category_db
from API_Products.database.db import get_db


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


def update_categories(dict_values: dict):
    if dict_values["new_name"].strip() == "":
        return dict(status=400, text="Valor inválido.")

    dict_values["new_name"] = dict_values["new_name"].capitalize()
    db = get_db()

    if False:
        pass
    # if db["category"].find_one({"name": dict_values["new_name"]}):
    #     return dict(status=400, text="O nome requerido já está sendo utilizado, não é possível atribuí-lo novamente.")
    else:
        # updated_category = category_db.update_categories_db(dict_values)
        updated_category = True
        if not updated_category:
            return dict(status=400, text="Não foi possível alterar a categoria.")
        else:
            db["book"].update_many({}, {"$set": {"category.$[element]": dict_values["new_name"]}}, False,
            [{"element": dict_values["old_name"]}])
            return dict(status=200, text="Categoria alterada com sucesso.")
            #
        # db.book.updateMany(
        #     {},
        #     {$set: {"category.$[element]": "Info"}},
        # {arrayFilters: [{"element": "Informática"}]}
        # )

print(update_categories(dict(old_name="Putaria", new_name="Putaria2")))