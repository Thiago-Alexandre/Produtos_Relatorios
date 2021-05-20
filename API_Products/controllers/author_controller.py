from database import author_db, country_db, book_db


def insert_author(dict_values: dict) -> dict:
    """
    Método para cadastrar novo autor.

    Verifica se os dados enviados são válidos. Retorna dados de erro caso estejam inválidos;
    Verifica se o autor já está cadastrado. Retorna dados de erro caso já esteja;
    Verifica se o país está cadastrado. Retorna dados de erro caso não esteja;
    Salva os dados do autor. Retorna mensagem de sucesso.
    Caso ocorra algum erro ao salvar, retorna dados de erro.

    :param dict_values: {name, lastname, country}
    :return: dict or raise Exception
    """
    received = set(dict_values.keys())
    expected = {"name", "lastname", "country"}

    if expected != received or not dict_values["name"] or not dict_values["lastname"] \
            or not dict_values["country"]:
        return dict(status=400, error="Valores inseridos inválidos.", message="Verifique os dados informados.")

    try:
        if author_db.validate_author(dict_values):
            return dict(status=400, error="Autor já salvo!", message="Verifique os dados informados.")
        if not country_db.search_country(dict_values['country']):
            return dict(status=400, error="País não foi encontrado!", message="Verifique os dados informados.")
        authors = author_db.insert_author_db(dict_values)
        return dict(status=200, result_data=authors)

    except Exception as error:
        return dict(status=400, error=error.args[0], message="Verifique os dados informados.")


def read_all_authors() -> dict:
    """
    Método para carregar os autores do banco.

    Retorna os dados dos autores pesquisados no banco.
    Caso ocorra algum erro ao pesquisar, retorna dados de erro.
    :return: dict
    """
    try:
        authors = author_db.read_all_authors_db()
        return dict(status=200, result_data=authors)
    except Exception as error:
        return dict(status=400, error=error.args[0], message="Tente novamente mais tarde.")


def update_author(dict_values) -> dict:
    """
    Método para alterar dados dos autores.

    Verifica se os dados enviados são válidos. Retorna dados de erro caso estejam inválidos;
    Verifica se o autor já está cadastrado. Retorna dados de erro caso já esteja;
    Verifica se o país está cadastrado. Retorna dados de erro caso não esteja;
    Altera os dados do autor nos livros caso ele esteja sendo usado;
    Altera os dados do autor. Retorna mensagem de sucesso.
    Caso ocorra algum erro ao alterar, retorna dados de erro.

    :param dict_values: {_id, name, lastname, country}
    :return: dict or raise Exception
    """
    received = set(dict_values.keys())
    expected = {"_id", "name", "lastname", "country"}
    if expected != received or not dict_values["_id"] or not dict_values["name"] or not dict_values["lastname"] \
            or not dict_values["country"]:
        return dict(status=400, error="Valores inseridos inválidos.", message="Verifique os dados informados.")

    try:
        if author_db.validate_author(dict(name=dict_values["name"], lastname=dict_values["lastname"],
                                          country=dict_values["country"])):
            return dict(status=400, error="Autor já salvo!", message="Verifique os dados informados.")
        if not country_db.search_country(dict_values['country']):
            return dict(status=400, error="País não foi encontrado!", message="Verifique os dados informados.")
        old_author = author_db.search_author(dict_values["_id"])
        authors = author_db.update_author_db(dict_values)
        book_db.update_all_authors_book_db(old_author, dict_values)
        return dict(status=200, result_data=authors)
    except Exception as error:
        return dict(status=400, error=error.args[0], message="Verifique os dados informados.")


def delete_author(dict_values: dict) -> dict:
    """
    Método para excluir um autor.

    Verifica se o autor está sendo utilizado em algum livro salvo. Retorna dados de erro caso esteja.
    Realiza a exclusão do autor. Retorna mensagem de sucesso.
    Caso ocorra algum erro ao pesquisar, retorna dados de erro.

    :param dict_values: {name, lastname, country}
    :return: dict or raise Exception
    """
    try:
        if author_db.exists_author(dict_values):
            raise Exception("O autor está sendo utilizado, não é possível deletá-lo.")
        authors = author_db.delete_authors_db(dict_values)
        return dict(status=200, result_data=authors)
    except Exception as error:
        return dict(status=400, error=error.args[0], message="Verifique os dados informados.")
