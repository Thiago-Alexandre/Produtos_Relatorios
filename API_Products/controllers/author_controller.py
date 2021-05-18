from database import author_db, country_db


def author_insert_validation(dict_values: dict):
    # Checks the body request:
    received = set(dict_values.keys())
    expected = {"name", "lastname", "country"}
    dict_response = dict(status=400, error="Valores inseridos inválidos.", message="Verifique os dados informados.")

    if not expected.issubset(received):
        return dict_response

    validations = [
        len(dict_values["name"]) > 0,
        len(dict_values["lastname"]) > 0,
        len(dict_values["country"]) > 0
    ]
    if not all(validations):
        return dict_response

    try:
        exist_country = country_db.search_country(dict_values["country"])
        if exist_country:
            text = author_db.insert_author_db(dict_values)
            print(text)
            return dict(status=200, result_data=text)
        else:
            return dict(status=400, error="O país não foi encontrado!", message="Verifique o dados informados.")
    except Exception as error:
        return dict(status=400, text=error.args[0], message="Verifique os dados informados.")


def author_read_all_validation():
    try:
        authors = author_db.read_all_authors_db()
        return dict(status=200, result_data=authors)
    except Exception as error:
        return dict(status=400, error=error.args[0], message="Tente novamente mais tarde.")


def delete_author(dict_values: dict) -> dict:
    try:
        if not author_db.exist_author(dict_values):
            authors = author_db.delete_authors_db(dict_values)
        else:
            raise Exception("Não foi possível deletar o autor.")
        return dict(status=200, result_data=authors)
    except Exception as error:
        return dict(status=400, error=error.args[0], message="O autor já está sendo utilizado.")
