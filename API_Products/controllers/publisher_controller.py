from database import publisher_db, book_db, country_db


def insert_publisher(dict_values: dict) -> dict:
    """
    Método para cadastrar nova editora.

    Verifica se os dados enviados são válidos. Retorna dados de erro caso estejam inválidos;
    Verifica se a editora já está cadastrada. Retorna dados de erro caso já esteja;
    Verifica se o país está cadastrado. Retorna dados de erro caso não esteja;
    Salva os dados da editora. Retorna mensagem de sucesso.
    Caso ocorra algum erro ao salvar, retorna dados de erro.

    :param dict_values: {name, country}
    :return: dict or raise Exception
    """
    received = set(dict_values.keys())
    expected = {"name", "country"}
    if expected != received or not dict_values["name"] or not dict_values["country"]:
        return dict(status=400, error="Valores inseridos inválidos.", message="Verifique os dados informados.")

    try:
        if publisher_db.validate_publisher(dict_values):
            return dict(status=400, error="Editora já salva!", message="Verifique os dados informados.")
        if not country_db.search_country(dict_values['country']):
            return dict(status=400, error="País não foi encontrado!", message="Verifique os dados informados.")
        publishers = publisher_db.insert_publishers_db(dict_values)
        return dict(status=200, result_data=publishers)

    except Exception as error:
        return dict(status=400, error=error.args[0], message="Verifique os dados informados.")


def read_all_publishers() -> dict:
    """
    Método para carregar as editoras do banco.

    Retorna os dados das editoras pesquisados no banco.
    Caso ocorra algum erro ao pesquisar, retorna dados de erro.
    :return: dict
    """
    try:
        publishers = publisher_db.read_all_publishers_db()
        return dict(status=200, result_data=publishers)
    except Exception as error:
        return dict(status=400, error=error.args[0], message="Tente novamente mais tarde.")


def update_publisher(dict_values) -> dict:
    """
    Método para alterar dados das editoras.

    Verifica se os dados enviados são válidos. Retorna dados de erro caso estejam inválidos;
    Verifica se a editora já está cadastrada. Retorna dados de erro caso já esteja;
    Verifica se o país está cadastrado. Retorna dados de erro caso não esteja;
    Altera os dados da editora nos livros caso ela esteja sendo usada;
    Altera os dados da editora. Retorna mensagem de sucesso.
    Caso ocorra algum erro ao alterar, retorna dados de erro.

    :param dict_values: {_id, name, country}
    :return: dict or raise Exception
    """
    received = set(dict_values.keys())
    expected = {"_id", "name", "country"}
    if expected != received or not dict_values["_id"] or not dict_values["name"] or not dict_values["country"]:
        return dict(status=400, error="Valores inseridos inválidos.", message="Verifique os dados informados.")

    try:
        if publisher_db.validate_publisher(dict(name=dict_values["name"], country=dict_values["country"])):
            return dict(status=400, error="Editora já salva!", message="Verifique os dados informados.")
        if not country_db.search_country(dict_values['country']):
            return dict(status=400, error="País não foi encontrado!", message="Verifique os dados informados.")
        old_publisher = publisher_db.search_publisher(dict_values["_id"])
        publishers = publisher_db.update_publisher_db(dict_values)
        book_db.update_all_publishers_book_db(old_publisher, dict_values)
        return dict(status=200, result_data=publishers)
    except Exception as error:
        return dict(status=400, error=error.args[0], message="Verifique os dados informados.")


def delete_publisher(dict_values: dict) -> dict:
    """
    Método para excluir uma editora.

    Verifica se a editora está sendo utilizada em algum livro salvo. Retorna dados de erro caso esteja.
    Realiza a exclusão da editora. Retorna mensagem de sucesso.
    Caso ocorra algum erro ao pesquisar, retorna dados de erro.

    :param dict_values: {name, country}
    :return: dict or raise Exception
    """
    try:
        if publisher_db.exists_publisher(dict_values):
            raise Exception("A editora está sendo utilizada, não é possível deletá-la.")
        publishers = publisher_db.delete_publishers_db(dict_values)
        return dict(status=200, result_data=publishers)
    except Exception as error:
        return dict(status=400, error=error.args[0], message="Verifique os dados informados.")
