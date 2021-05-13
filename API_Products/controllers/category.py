from API_Products.database import category_db, db


def read_all_categories() -> dict:
    try:
        categories = category_db.read_all()
        return dict(status=200, text=categories)
    except Exception as error:
        return dict(status=400, text=error)


def insert_categories(dict_values: dict) -> dict:

    if dict_values["name"].strip() == "":
        return dict(status=400, text="Valor inválido.")

    validate_category = db.DB["category"].count_documents(dict_values, {})

    if not validate_category > 0:
        try:
            category_db.insert(dict_values)
            return dict(status=200, text="Cadastrado com sucesso.")
        except Exception as error:
            return dict(status=400, text=f"Não foi possível cadastrar a categoria.{error}")

    else:
        return dict(status=400, text="Categoria já cadastrada.")

