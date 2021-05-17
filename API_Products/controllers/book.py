from database import book_db
from datetime import datetime


def insert_book(dict_values: dict) -> dict:
    try:
        insert_book_validations(dict_values)
        book_db.insert_book_db(dict_values)
        return dict(status=200, text="Livro cadastrado com sucesso!")
    except Exception as error:
        return dict(status=400, text=f"{error}")


def insert_book_validations(dict_values: dict):

    if float(dict_values['item_price']) <= 0:
        raise Exception("O preço deve ser maior que zero.")
    elif int(dict_values['item_quantity']) < 0:
        raise Exception("A quantidade de livros deve ser maior ou igual a zero.")
    elif int(dict_values['page_quantity']) <= 0:
        raise Exception("A quantidade de páginas do livro deve ser maior que zero.")

    list_of_material_books = ['Físico', 'Braille']
    if dict_values['format'] in list_of_material_books:
        if float(dict_values['weight']) <= 0:
            raise Exception("O peso de um livro físico deve ser maior que zero.")
        elif float(dict_values['size']['height']) <= 0:
            raise Exception("A altura de um livro físico deve ser maior que zero.")
        elif float(dict_values['size']['lenght']) <= 0:
            raise Exception("O comprimento de um livro físico deve ser maior que zero.")
        elif float(dict_values['size']['width']) <= 0:
            raise Exception("A largura de um livro físico deve ser maior que zero.")

    if datetime.strptime(dict_values['published_at'], "%d/%m/%Y") > datetime.today():
        raise Exception("A data de publicação é inválida.")

    if isinstance(dict_values['isbn-10'], str) and len(dict_values['isbn-10']) == 10:
        if book_db.isbn_exists_db(dict_values['isbn-10']):
            raise Exception("Isbn 10 já cadastrado.")
    else:
        raise Exception("Formato inválido!")

    if isinstance(dict_values['isbn-13'], str) and len(dict_values['isbn-13']) == 13:
        if book_db.isbn_exists_db(dict_values['isbn-13']):
            raise Exception("Isbn 13 já cadastrado.")
    else:
        raise Exception("Formato inválido!")


def add_comment_book(comment_values: dict):
    try:
        book = book_db.search_book_for_id(comment_values["id_book"])
        book["comments"].append(comment_values["comment"])
        total_classification = 0
        quantity_comments = len(book["comments"])
        for c in book["comments"]:
            total_classification += c["classification"]
        book["rating"] = total_classification / quantity_comments
        book_db.update_book(book)
        return dict(status=200, text="Comentário adicionado com sucesso!")
    except Exception as error:
        return dict(status=400, text=f"Erro: {error}")