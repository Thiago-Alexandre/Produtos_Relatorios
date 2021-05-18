from database import author_db, country_db


def author_insert_validation(dict_values: dict):
    try:
        exist_country = country_db.search_country(dict_values["country"])
        if exist_country:
            text = author_db.insert_author_db(dict_values)
            return dict(status=200, text=text)
        else:
            return dict(status=400, text="O país não foi encontrado!")
    except Exception as error:
            return dict(status=400, text=error.args[0])


def author_read_all_validation():
        try:
            authors = author_db.read_all_authors_db()
            return dict(status=200, text=authors)
        except Exception as error:
            return dict(status=400, text=error.args[0])


def delete_author(dict_values: dict) -> dict:
    try:
        if not author_db.exist_author(dict_values):
            authors = author_db.delete_authors_db(dict_values)
        else:
            raise Exception("O autor já está sendo utilizado, não é possível deletá-lo agora.")
        return dict(status=200, text=authors)
    except Exception as error:
        return dict(status=400, text=error.args[0])
