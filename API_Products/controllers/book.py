from API_Products.database import book_db
from datetime import datetime


def insert_book(dict_values: dict) -> dict:
    try:
        insert_book_validations(dict_values)
        dict_values["reserve_quantity"] = 0
        book_db.insert_book_db(dict_values)
        return dict(status=200, message="Livro cadastrado com sucesso!")
    except Exception as error:
        return dict(status=400, error=error.args[0], message="Verifique os dados informados.")


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

        
def verify_stock(list_shopping_cart_values):
    list_books_values = book_db.search_books_for_id(list_shopping_cart_values)
    list_rejected_items = []
    total_price_items = 0.0
    digital_value = True

    for i in range(len(list_shopping_cart_values)):
        if list_shopping_cart_values[i]["quantity_purchased"] <= list_books_values[i]["item_quantity"]:
            total_price_items += list_books_values[i]["item_price"]
            if not list_books_values[i]["format"]["digital"]:
                digital_value = False
        else:
            list_shopping_cart_values[i]["quantity_purchased"] = list_books_values[i]["item_quantity"]
            list_rejected_items.append(list_shopping_cart_values[i])

    if list_rejected_items:
        return dict(status=400, books_lacking=list_rejected_items, stocks=False)
    else:
        reserve_books(list_shopping_cart_values, list_books_values)
        return dict(status=200, books_stocks=list_books_values, stocks=True, total_price=total_price_items, digital=digital_value)


def reserve_books(list_shopping_cart_values, list_books_values):
    for i in range(len(list_shopping_cart_values)):
        list_books_values[i]["item_quantity"] -= list_shopping_cart_values[i]["quantity_purchased"]
        list_books_values[i]["reserve_quantity"] += list_shopping_cart_values[i]["quantity_purchased"]
    try:
        for dict_values in list_books_values:
            book_db.update_book_db(dict_values)
    except Exception as error:
        return f"Erro: {error.args[0]}"
    return "Reserva realizada com sucesso!"


def finish_purshase(books_cart: list, success: bool) -> dict:
    try:
        books_saved = book_db.search_books_for_id(books_cart)
        for i in range(len(books_saved)):
            if not success:
                books_saved[i]["item_quantity"] += books_cart[i]["quantity_purchased"]
            books_saved[i]["reserve_quantity"] -= books_cart[i]["quantity_purchased"]
            book_db.update_book_db(books_saved[i])
    except Exception as error:
        return dict(status=400, text=f"Erro: {error.args[0]}")
    return dict(status=200, text="Estoque alterado com sucesso!")