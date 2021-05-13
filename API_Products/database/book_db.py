from additionals.functions import convert_object_id_to_string
from db import DB


def insert_book(dict_values: dict):

    if dict_values:
        DB.book.insert_one(dict_values)
        return "Registrado com sucesso!"
    else:
        raise Exception("Registros inválidos.")


def read_all() -> list:

    book = DB.book.find()
    book_list = convert_object_id_to_string(book)

    if book_list:
        return book_list
    else:
        raise Exception("Nenhum livro encontrado!")

print(read_all())