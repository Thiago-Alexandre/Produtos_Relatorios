from datetime import datetime

from database.book_db import isbn_exists_db, get_books_by_id
from database.author_db import read_all_authors_db
from database.category_db import read_all_categories_db
from database.format_db import get_book_format_list_db
from database.language_book_db import get_language_book_list_db
from database.publisher_db import read_all_publishers_db


def validate_book(body_request: dict, is_update=False):
    # Expected body request:
    expected = {
        "_id",
        "title",
        "description",
        "language_book",
        "category",
        "author",
        "edition",
        "publisher",
        "isbn-10",
        "isbn-13",
        "format",
        "published_at",
        "item_price",
        "item_quantity",
        "item_cost_price",
        "size",
        "weight",
        "page_quantity"
    }
    expected_author = {"name", "lastname", "country"}
    expected_publisher = {"name", "country"}
    expected_size = {"height", "lenght", "width"}
    received = set(body_request.keys())

    if not is_update:
        expected.discard("_id")

    # BODY REQUEST VALIDATION:
    error_message = "Invalid body request."
    default_message = "Verifique se todos os dados foram informados. "

    if expected != received:
        missing_keys = expected - received
        default_message += f"Keys faltantes: {', '.join(missing_keys)}."

        raise Exception(error_message, default_message)

    # Validates the author information:
    if not isinstance(body_request["author"], list) or \
            len(body_request["author"]) == 0 or \
            not all(isinstance(val, dict) for val in body_request["author"]):

        default_message = "Dados do autor devem ser uma lista de dicionários."
        raise Exception(error_message, default_message)

    elif expected_author != set(body_request["author"][0].keys()):
        missing_keys = expected_author - set(body_request["author"][0].keys())
        default_message += f"Keys faltantes: {', '.join(missing_keys)}."
        error_message = "Dados do autor incompletos."
        raise Exception(error_message, default_message)

    # Validates the publisher information:
    if not isinstance(body_request["publisher"], dict):
        default_message = "Dados da editora devem ser um dicionário."
        raise Exception(error_message, default_message)

    elif expected_publisher != set(body_request["publisher"].keys()):
        missing_keys = expected_publisher - set(body_request["publisher"].keys())
        default_message += f"Keys faltantes: {', '.join(missing_keys)}."

        raise Exception(error_message, default_message)

    # Validate sizes information:
    if type(body_request["size"]) is not dict:
        default_message = "Dados do tamanho do livro devem ser um dicionário."
        raise Exception(error_message, default_message)

    elif expected_size != set(body_request["size"].keys()):
        missing_keys = expected_size - set(body_request["size"].keys())
        default_message += f"Keys faltantes: {', '.join(missing_keys)}."
        raise Exception(error_message, default_message)

    # VALIDATION OF THE VALUES PASSED IN THE REQUEST BODY:
    if len(str(body_request["title"])) == 0:
        default_message = "Verifique o título informado."
        raise Exception(error_message, default_message)

    if len(str(body_request["description"])) == 0:
        default_message = "Verifique a descrição informada."
        raise Exception(error_message, default_message)

    if len(str(body_request["language_book"])) == 0:
        default_message = "Verifique o idioma informado."
        raise Exception(error_message, default_message)

    if not isinstance(body_request["edition"], int) or body_request["edition"] <= 0:
        default_message = "A edição deve ser um número inteiro maior que zero."
        raise Exception(error_message, default_message)

    try:
        pub_date = datetime.fromisoformat(body_request["published_at"])
        if pub_date > datetime.now():
            default_message = "A data de lançamento informada não é válida."
            raise Exception(error_message, default_message)
    except Exception:
        default_message = "A data deve estar em formato ISO: YYYY-mm-dd."
        raise Exception(error_message, default_message)

    try:
        item_price = float(body_request["item_price"])
        if item_price <= 0:
            default_message = "O preço do produto deve ser maior que zero."
            raise Exception(error_message, default_message)
    except Exception:
        default_message = "O preço do produto deve ser numérico."
        raise Exception(error_message, default_message)

    try:
        item_cost_price = float(body_request["item_cost_price"])
        if item_cost_price <= 0:
            default_message = "O preço de custo do produto deve ser maior que zero."
            raise Exception(error_message, default_message)
    except Exception:
        default_message = "O preço de custo do produto deve ser numérico."
        raise Exception(error_message, default_message)

    if item_cost_price > item_price:
        default_message = "O preço de venda deve ser maior que o preço de custo."
        raise Exception(error_message, default_message)

    if not isinstance(body_request["item_quantity"], int) or body_request["item_quantity"] < 0:
        default_message = "A quantidade do produto deve ser maior que zero."
        raise Exception(error_message, default_message)

    try:
        float(body_request["weight"])
    except ValueError:
        default_message = "O peso deve ser um valor numérico."
        raise Exception(error_message, default_message)

    if not isinstance(body_request["page_quantity"], int) and not body_request["page_quantity"] > 0:
        default_message = "A quantidade de páginas deve ser um número maior que zero."
        raise Exception(error_message, default_message)

    language_book_list = list(x['name'] for x in get_language_book_list_db())
    if body_request["language_book"] not in language_book_list:
        default_message = "O idioma inserido não existe."
        raise Exception(error_message, default_message)

    author_list = list(filter(lambda x: x.pop("_id"), read_all_authors_db()))
    for author in body_request["author"]:
        if author not in author_list:
            default_message = "Os dados do autor estão incorretos."
            raise Exception(error_message, default_message)

    publisher_list = list(filter(lambda x: x.pop("_id"), read_all_publishers_db()))
    if body_request["publisher"] not in publisher_list:
        default_message = "Os dados da editora estão incorretos."
        raise Exception(error_message, default_message)

    fisical_book_formats = get_book_format_list_db()
    if body_request["format"] not in list(x["name"] for x in fisical_book_formats if not x["digital"]):
        default_message = "Verifique o formato do livro especificado."
        raise Exception(error_message, default_message)

    category_list = {x['name'] for x in read_all_categories_db()}
    if not isinstance(body_request["category"], list) or not set(body_request["category"]).issubset(category_list):
        default_message = "Verifique os dados da categoria informados."
        raise Exception(error_message, default_message)

    if not is_update:
        if isinstance(body_request["isbn-10"], str):
            isbn_10 = "".join([x for x in body_request['isbn-10'] if x.isdigit()])
            if len(isbn_10) != 10:
                default_message = "Verifique o ISBN-10 informado."
                raise Exception(error_message, default_message)
            elif isbn_exists_db(isbn_10):
                error_message = "Cadastro não efetuado."
                default_message = "Já existe um livro com este ISBN-10 cadastrado."
                raise Exception(error_message, default_message)
        else:
            default_message = "Verifique o ISBN-10 informado."
            raise Exception(error_message, default_message)

        if isinstance(body_request["isbn-13"], str):
            isbn_13 = "".join([x for x in body_request['isbn-13'] if x.isdigit()])
            if len(isbn_13) != 13:
                default_message = "Verifique o ISBN-13 informado."
                raise Exception(error_message, default_message)
            elif isbn_exists_db(isbn_13):
                error_message = "Cadastro não efetuado."
                default_message = "Já existe um livro com este ISBN-13 cadastrado."
                raise Exception(error_message, default_message)
        else:
            default_message = "Verifique o ISBN-10 informado."
            raise Exception(error_message, default_message)
    else:
        isbns = get_books_by_id(body_request["_id"], **{"isbn-10": 1, "isbn-13": 1})[0]
        if isbns["isbn-10"] != body_request["isbn-10"] or isbns["isbn-13"] != body_request["isbn-13"]:
            raise Exception("Não é possível mudar o ISBN.", "Verififque os ISBN's informados.")
