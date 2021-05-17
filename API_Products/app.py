from flask import Flask, request
from API_Products.controllers import category, publisher, author_controller, book
from API_Products.database.auth import KEYS

app = Flask(__name__)

#Rotas categorias


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


@app.route("/delete_categories", methods=["DELETE"])
def delete_categories():
    header = dict(request.headers)
    if header["Senha"] not in KEYS:
        return dict(text="Chave de acesso inválida."), 400
    dict_values = request.get_json()
    category_deleted = category.delete_categories(dict_values)
    status = category_deleted["status"]
    del category_deleted["status"]

    return category_deleted, status

#Rotas editoras


@app.route("/read_publishers", methods=["GET"])
def read_publishers():
    header = dict(request.headers)
    if header["Senha"] not in KEYS:
        return dict(text="Chave de acesso inválida."), 400
    publishers = publisher.read_all_publishers()
    status = publishers["status"]
    del publishers["status"]

    return publishers, status


@app.route("/insert_publishers", methods=["POST"])
def insert_publishers():
    header = dict(request.headers)
    if header["Senha"] not in KEYS:
        return dict(text="Chave de acesso inválida."), 400
    dict_values = request.get_json()
    publishers = publisher.insert_publisher(dict_values)
    status = publishers["status"]
    del publishers["status"]

    return publishers, status

#Rotas autores


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

#Rotas livros


@app.route("/insert_books", methods=["POST"])
def insert_books():
    header = dict(request.headers)
    if header["Senha"] not in KEYS:
        return dict(text="Chave de acesso inválida."), 400
    dict_values = request.get_json()
    books = book.insert_book(dict_values)
    status = books["status"]
    del books["status"]

    return books, status


app.run(debug=True)