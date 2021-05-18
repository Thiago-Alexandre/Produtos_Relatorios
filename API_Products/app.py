from flask import Flask, request

from book_logs.book_logs import generate_log_data
from book_logs.logging_db import insert_log_db
from controllers import category, publisher_controller, author_controller, book
from database.auth import KEYS

app = Flask(__name__)


@app.route("/read_categories", methods=["GET"])
def read_categories():
    header = dict(request.headers)
    if header["Senha"] not in KEYS:
        return dict(text="Chave de acesso inválida."), 400
    categories = category.read_all_categories()
    status = categories["status"]
    del categories["status"]

    return categories, status


@app.route("/insert_categories", methods=["POST"])
def insert_categories():
    header = dict(request.headers)
    if header["Senha"] not in KEYS:
        return dict(text="Chave de acesso inválida."), 400
    dict_values = request.get_json()
    categories = category.insert_categories(dict_values)
    status = categories["status"]
    del categories["status"]

    return categories, status


@app.route("/read_publishers", methods=["GET"])
def read_publishers():
    header = dict(request.headers)
    if header["Senha"] not in KEYS:
        return dict(text="Chave de acesso inválida."), 400
    publishers = publisher_controller.read_all_publishers()
    status = publishers["status"]
    del publishers["status"]

    return publishers, status


@app.route("/insert_publishers", methods=["POST"])
def insert_publishers():
    header = dict(request.headers)
    if header["Senha"] not in KEYS:
        return dict(text="Chave de acesso inválida."), 400
    dict_values = request.get_json()
    publishers = publisher_controller.insert_publisher(dict_values)
    status = publishers["status"]
    del publishers["status"]

    return publishers, status


@app.route("/read_authors", methods=["GET"])
def read_author():
    header = dict(request.headers)
    if header["Senha"] not in KEYS:
        return dict(text="Chave de acesso inválida."), 400
    authors = author_controller.author_read_all_validation()
    status = authors["status"]
    del authors["status"]

    return authors, status


@app.route("/insert_authors", methods=["POST"])
def insert_authors():
    header = dict(request.headers)
    if header["Senha"] not in KEYS:
        return dict(text="Chave de acesso inválida."), 400
    dict_values = request.get_json()
    authors = author_controller.author_insert_validation(dict_values)
    status = authors["status"]
    del authors["status"]

    return authors, status


@app.route("/insert_books", methods=["POST"])
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


app.run(debug=True)
