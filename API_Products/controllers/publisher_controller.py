from database import publisher_db, book_db, country_db


def insert_publisher(dict_values: dict) -> dict:
    received = set(dict_values.keys())
    expected = {"name", "country"}
    if not expected.issubset(received) or not dict_values["name"] or not dict_values["country"]:
        return dict(status=400, error="Valores inseridos inválidos.", message="Verifique os dados informados.")

    try:
        exist_country = country_db.search_country(dict_values['country'])
        if exist_country:
            publishers = publisher_db.insert_publishers_db(dict_values)
            return dict(status=200, result_data=publishers)
        return dict(status=400, error="País não foi encontrado!", message="Verifique os dados informados.")
    except Exception as error:
        return dict(status=400, error=error.args[0], message="Verifique os dados informados.")


def read_all_publishers() -> dict:
    try:
        publishers = publisher_db.read_all_publishers_db()
        return dict(status=200, result_data=publishers)
    except Exception as error:
        return dict(status=400, error=error.args[0], message="Tente novamente mais tarde.")


def update_publisher(dict_values) -> dict:
    received = set(dict_values.keys())
    expected = {"_id", "name", "country"}
    if not expected.issubset(received) or not dict_values["_id"] or \
            not dict_values["name"] or not dict_values["country"]:
        return dict(status=400, error="Valores inseridos inválidos.", message="Verifique os dados informados.")

    try:
        if not publisher_db.validate_publisher(dict_values):
            old_publisher = publisher_db.search_publisher(dict_values["_id"])
            book_db.update_all_publishers_book_db(old_publisher["name"], dict_values['name'])
            publishers = publisher_db.update_publisher_db(dict_values)
            return dict(status=200, result_data=publishers)
        else:
            raise Exception("O nome requerido já está sendo utilizado, não é possível atribuí-lo novamente.")
    except Exception as error:
        return dict(status=400, error=error.args[0], message="Verifique os dados informados.")


def delete_publisher(dict_values: dict) -> dict:
    try:
        if not publisher_db.exists_publisher(dict_values):
            publishers = publisher_db.delete_publishers_db(dict_values)
            return dict(status=200, result_data=publishers)
        else:
            raise Exception("A editora está sendo utilizada, não é possível deletá-la.")
    except Exception as error:
        return dict(status=400, error=error.args[0], message="Verifique os dados informados.")


def publisher_dict_validate(dict_values: dict) -> bool:
    received = set(dict_values.keys())
    expected = {"_id", "name", "country"}
    if not expected.issubset(received) or not dict_values["name"] or not dict_values["country"]:
        return False
    return True
