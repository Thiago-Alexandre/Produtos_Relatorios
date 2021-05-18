from flask import Flask, request

from book_logs.book_logs import generate_log_data
from book_logs.logging_db import insert_log_db
from controllers import category, publisher_controller, author_controller, book, country_controller, \
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


@app.route("/authors", methods=["GET"])
def read_author():
    header = dict(request.headers)

    if "Access-Key" not in list(header.keys()) or header.get("Access-Key") not in list(KEYS.values()):
        response = dict(status=400, error="Chave de acesso inválida.", message="Verifique os dados informados.")
    else:
        response = author_controller.author_read_all_validation()

    return response, response["status"]


@app.route("/authors/new", methods=["POST"])
def insert_authors():
    header = dict(request.headers)

    if "Access-Key" not in list(header.keys()) or header.get("Access-Key") not in list(KEYS.values()):
        response = dict(status=400, error="Chave de acesso inválida.", message="Verifique os dados informados.")
    else:
        dict_values = request.get_json()
        response = author_controller.author_insert_validation(dict_values)

    return response, response["status"]


@app.route("/books/new", methods=["POST"])
def insert_books():
    header = dict(request.headers)

    if "Access-Key" not in list(header.keys()) or header.get("Access-Key") not in list(KEYS.values()):
        response = dict(status=400, error="Chave de acesso inválida.", message="Verifique os dados informados.")
    else:
        body_request = request.get_json()
        response = book.insert_book(body_request)

    try:
        log_data = generate_log_data(request, response)
        insert_log_db(log_data)
    except Exception as err:
        print(err.args[0])

    return response, response["status"]


@app.route("/books", methods=["GET"])
def read_books():
    header = dict(request.headers)

    if "Access-Key" not in list(header.keys()) or header.get("Access-Key") not in list(KEYS.values()):
        response = dict(status=400, error="Chave de acesso inválida.", message="Verifique os dados informados.")
    else:
        response = book.get_book_list()

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

    try:
        log_data = generate_log_data(request, response)
        insert_log_db(log_data)
    except Exception as err:
        print("Logging error: " + err.args[0])

    return response, response["status"]


@app.route("/languages", methods=["GET"])
def read_language_books():
    header = dict(request.headers)

    if "Access-Key" not in list(header.keys()) or header.get("Access-Key") not in list(KEYS.values()):
        response = dict(status=400, error="Chave de acesso inválida.", message="Verifique os dados informados.")
    else:
        response = language_book_controller.get_language_book_list()

    try:
        log_data = generate_log_data(request, response)
        insert_log_db(log_data)
    except Exception as err:
        print("Logging error: " + err.args[0])

    return response, response["status"]


@app.route("/formats", methods=["GET"])
def read_format_books():
    header = dict(request.headers)

    if "Access-Key" not in list(header.keys()) or header.get("Access-Key") not in list(KEYS.values()):
        response = dict(status=400, error="Chave de acesso inválida.", message="Verifique os dados informados.")
    else:
        response = format_controller.get_format_list()

    try:
        log_data = generate_log_data(request, response)
        insert_log_db(log_data)
    except Exception as err:
        print("Logging error: " + err.args[0])

    return response, response["status"]


app.run(debug=True)
