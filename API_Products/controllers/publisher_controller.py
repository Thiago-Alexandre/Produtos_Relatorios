from database import publisher_db, book_db, country_db


def insert_publisher(dict_values: dict) -> dict:
    # Checks the body request:
    received = set(dict_values.keys())
    expected = {"name", "country"}
    dict_response = dict(status=400, error="Valores inseridos inválidos.", message="Verifique os dados informados.")
    if not expected.issubset(received):
        return dict_response
    elif len(dict_values["name"]) > 0 or len(dict_values["country"]) > 0:
        return dict_response

    try:
        exist_country = country_db.search_country(dict_values['country'])

        if exist_country:
            publishers = publisher_db.insert_publishers_db(dict_values)
            return dict(status=200, result_data=publishers)
        else:
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
    try:
        if not publisher_db.validate_publisher(dict_values['name']):
            publishers = publisher_db.update_publisher_db(dict_values['name'])
            book_db.update_all_publishers_book_db(dict_values['name'], dict_values['new_value'])
            return dict(status=200, text=publishers)
        else:
            raise Exception("O nome requerido já está sendo utilizado, não é possível atribuí-lo novamente.")
    except Exception as error:
        return dict(status=400, text=error.args[0])


def delete_publisher(dict_values: dict) -> dict:
    try:
        if not publisher_db.exists_publisher(dict_values):
            publishers = publisher_db.delete_publishers_db(dict_values)
            return dict(status=200, text=publishers)
        else:
            raise Exception("A editora está sendo utilizada, não é possível deletá-la.")
    except Exception as error:
        return dict(status=400, text=error.args[0])
