from flask import Flask, request

from book_logs.book_logs import generate_log_data
from book_logs.logging_db import *
from controllers import category, publisher_controller, author_controller, book_controller, country_controller, \
    language_book_controller, format_controller
from database.auth import KEYS

app = Flask(__name__)


@app.route("/categories", methods=["GET"])
def read_categories():
    header = dict(request.headers)

    if "Access-Key" not in list(header.keys()) or header.get("Access-Key") not in list(KEYS.values()):
        response = dict(status=400, error="Chave de acesso inválida.", message="Verifique os dados informados.")
    else:
        response = category.read_all_categories()

    return response, response["status"]


@app.route("/categories/new", methods=["POST"])
def insert_categories():
    header = dict(request.headers)

    if "Access-Key" not in list(header.keys()) or header.get("Access-Key") not in list(KEYS.values()):
        response = dict(status=400, error="Chave de acesso inválida.", message="Verifique os dados informados.")
    else:
        dict_values = request.get_json()
        response = category.insert_categories(dict_values)

    return response, response["status"]


@app.route("/categories/update", methods=["PUT"])
def update_categories():
    header = dict(request.headers)

    if "Access-Key" not in list(header.keys()) or header.get("Access-Key") not in list(KEYS.values()):
        response = dict(status=400, error="Chave de acesso inválida.", message="Verifique os dados informados.")
    else:
        dict_values = request.get_json()
        response = category.update_categories(dict_values)

    return response, response["status"]


@app.route("/categories/delete", methods=["DELETE"])
def delete_categories():
    header = dict(request.headers)

    if "Access-Key" not in list(header.keys()) or header.get("Access-Key") not in list(KEYS.values()):
        response = dict(status=400, error="Chave de acesso inválida.", message="Verifique os dados informados.")
    else:
        dict_values = request.get_json()
        response = category.delete_categories(dict_values)

    return response, response["status"]


@app.route("/publishers", methods=["GET"])
def read_publishers():
    header = dict(request.headers)

    if "Access-Key" not in list(header.keys()) or header.get("Access-Key") not in list(KEYS.values()):
        response = dict(status=400, error="Chave de acesso inválida.", message="Verifique os dados informados.")
    else:
        response = publisher_controller.read_all_publishers()

    return response, response["status"]


@app.route("/publishers/new", methods=["POST"])
def insert_publishers():
    header = dict(request.headers)

    if "Access-Key" not in list(header.keys()) or header.get("Access-Key") not in list(KEYS.values()):
        response = dict(status=400, error="Chave de acesso inválida.", message="Verifique os dados informados.")
    else:
        dict_values = request.get_json()
        response = publisher_controller.insert_publisher(dict_values)

    return response, response["status"]


@app.route("/publishers/update", methods=["PUT"])
def update_publishers():
    header = dict(request.headers)

    if "Access-Key" not in list(header.keys()) or header.get("Access-Key") not in list(KEYS.values()):
        response = dict(status=400, error="Chave de acesso inválida.", message="Verifique os dados informados.")
    else:
        dict_values = request.get_json()
        response = publisher_controller.update_publisher(dict_values)

    return response, response["status"]


@app.route("/publishers/delete", methods=["DELETE"])
def delete_publishers():
    header = dict(request.headers)

    if "Access-Key" not in list(header.keys()) or header.get("Access-Key") not in list(KEYS.values()):
        response = dict(status=400, error="Chave de acesso inválida.", message="Verifique os dados informados.")
    else:
        dict_values = request.get_json()
        response = publisher_controller.delete_publisher(dict_values)

    return response, response["status"]


@app.route("/authors", methods=["GET"])
def read_author():
    header = dict(request.headers)

    if "Access-Key" not in list(header.keys()) or header.get("Access-Key") not in list(KEYS.values()):
        response = dict(status=400, error="Chave de acesso inválida.", message="Verifique os dados informados.")
    else:
        response = author_controller.read_all_authors()

    return response, response["status"]


@app.route("/authors/new", methods=["POST"])
def insert_authors():
    header = dict(request.headers)

    if "Access-Key" not in list(header.keys()) or header.get("Access-Key") not in list(KEYS.values()):
        response = dict(status=400, error="Chave de acesso inválida.", message="Verifique os dados informados.")
    else:
        dict_values = request.get_json()
        response = author_controller.insert_author(dict_values)

    return response, response["status"]


@app.route("/authors/update", methods=["PUT"])
def update_authors():
    header = dict(request.headers)

    if "Access-Key" not in list(header.keys()) or header.get("Access-Key") not in list(KEYS.values()):
        response = dict(status=400, error="Chave de acesso inválida.", message="Verifique os dados informados.")
    else:
        dict_values = request.get_json()
        response = author_controller.update_author(dict_values)

    return response, response["status"]


@app.route("/authors/delete", methods=["DELETE"])
def delete_authors():
    header = dict(request.headers)

    if "Access-Key" not in list(header.keys()) or header.get("Access-Key") not in list(KEYS.values()):
        response = dict(status=400, error="Chave de acesso inválida.", message="Verifique os dados informados.")
    else:
        dict_values = request.get_json()
        response = author_controller.delete_author(dict_values)
        
    return response, response["status"]


@app.route("/books/new", methods=["POST"])
def insert_books():
    header = dict(request.headers)

    if "Access-Key" not in list(header.keys()) or header.get("Access-Key") not in list(KEYS.values()):
        response = dict(status=400, error="Chave de acesso inválida.", message="Verifique os dados informados.")
    else:
        body_request = request.get_json()
        response = book_controller.insert_book(body_request)

    try:
        log_data = generate_log_data(request, response)
        insert_log_db(log_data)
    except Exception as err:
        print(err.args[0])

    return response, response.get("status")


@app.route("/books", methods=["GET"])
def read_books():
    header = dict(request.headers)

    if "Access-Key" not in list(header.keys()) or header.get("Access-Key") not in list(KEYS.values()):
        response = dict(status=400, error="Chave de acesso inválida.", message="Verifique os dados informados.")
    else:
        response = book_controller.get_book_list()

    try:
        log_data = generate_log_data(request, response)
        insert_log_db(log_data)
    except Exception as err:
        print("Logging error: " + err.args[0])

    return response, response["status"]


@app.route("/countries", methods=["GET"])
def read_countries():
    header = dict(request.headers)

    if "Access-Key" not in list(header.keys()) or header.get("Access-Key") not in list(KEYS.values()):
        response = dict(status=400, error="Chave de acesso inválida.", message="Verifique os dados informados.")
    else:
        response = country_controller.get_country_name_list()

    return response, response["status"]


@app.route("/languages", methods=["GET"])
def read_language_books():
    header = dict(request.headers)

    if "Access-Key" not in list(header.keys()) or header.get("Access-Key") not in list(KEYS.values()):
        response = dict(status=400, error="Chave de acesso inválida.", message="Verifique os dados informados.")
    else:
        response = language_book_controller.get_language_book_list()

    return response, response["status"]


@app.route("/formats", methods=["GET"])
def read_format_books():
    header = dict(request.headers)

    if "Access-Key" not in list(header.keys()) or header.get("Access-Key") not in list(KEYS.values()):
        response = dict(status=400, error="Chave de acesso inválida.", message="Verifique os dados informados.")
    else:
        response = format_controller.get_format_list()

    return response, response["status"]


@app.route("/books/stock/verify", methods=["GET"])
def verify_stock():
    header = dict(request.headers)
    body_request = request.get_json()

    default_message = "Verifique se todos os dados foram informados."

    if "Access-Key" not in list(header.keys()) or header.get("Access-Key") not in list(KEYS.values()):
        response = dict(status=400, error="Chave de acesso inválida.", message=default_message)

    try:
        response = book_controller.verify_stock(body_request)
    except Exception:
        response = dict(status=400, error="Erro ao verificar estoque.", message=default_message)

    try:
        log_data = generate_log_data(request, response)
        insert_log_db(log_data)
    except Exception as err:
        print(err.args[0])

    return response, response["status"]


@app.route("/books/purchase/finish", methods=["POST"])
def finish_purchase():
    header = dict(request.headers)
    body_request = request.get_json()

    default_error = "Dados inválidos."
    default_message = "Verifique os dados informados."

    if "Access-Key" not in list(header.keys()) or header.get("Access-Key") not in list(KEYS.values()):
        response = dict(status=400, error="Chave de acesso inválida.", message=default_message)

    # Validates body request:
    expected = {"shopping_car", "purchased"}
    received = set(body_request.keys())
    if expected != received:
        response = dict(status=400, error=default_error, message=default_message)
    elif not isinstance(body_request["purchased"], bool):
        response = dict(status=400, error=default_error, message=default_message)

    try:
        response = book_controller.finish_purchase(body_request["shopping_car"], body_request["purchased"])
    except Exception:
        response = dict(status=400, error="Erro ao finalizar a compra.", message=default_message)

    try:
        log_data = generate_log_data(request, response)
        insert_log_db(log_data)
    except Exception as err:
        print(err.args[0])

    return response, response["status"]


app.run(debug=True)
