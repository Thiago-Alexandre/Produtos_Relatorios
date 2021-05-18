from flask import Flask, request

from API_Products.controllers import category, publisher_controller, author_controller, book
from API_Products.database.auth import KEYS

from book_logs.book_logs import generate_log_data
from book_logs.logging_db import insert_log_db

app = Flask(__name__)

#Rotas categorias


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


@app.route("/categories/delete", methods=["DELETE"])
def delete_categories():
    header = dict(request.headers)
    if header["Senha"] not in KEYS:
        return dict(text="Chave de acesso inválida."), 400
    dict_values = request.get_json()
    category_deleted = category.delete_categories(dict_values)
    status = category_deleted["status"]
    del category_deleted["status"]

    return category_deleted, status


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


app.run(debug=True)
