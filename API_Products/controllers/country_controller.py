from database.country_db import get_country_name_list_db


def get_country_name_list():
    try:
        result_data = get_country_name_list_db()

        if result_data:
            return dict(status=200, result_data=result_data)
        else:
            raise Exception("Não foi possível acessar a base de dados!")
    except Exception as error:
        return dict(status=500, error=error.args[0], message="Tente novamente mais tarde.")
