from controllers.utils import validate_book
from database import book_db


def insert_book(dict_values: dict) -> dict:
    try:
        validate_book(dict_values)
    except Exception as error:
        return dict(status=400, error=error.args[0], message=error.args[1])

    try:
        dict_values["reserve_quantity"] = 0

        inserted_book = book_db.insert_book_db(dict_values)

        return dict(status=200, message="Livro cadastrado com sucesso!", book=inserted_book)
    except Exception as error:
        return dict(status=500, error=error.args[0], message=error.args[1])


def get_book_list() -> dict:
    try:
        result_data = book_db.read_all_books_db()

        if result_data:
            return dict(status=200, result_data=result_data)
        else:
            return dict(status=200, message="Nenhum livro cadastrado.", result_data=[])
    except Exception as error:
        return dict(status=500, error=error.args[0], message="Tente novamente mais tarde.")


def verify_stock(list_shopping_cart_values):
    list_ids = list(map(lambda x: x['_id'], list_shopping_cart_values))

    list_books_values = book_db.search_books_by_id(*list_ids)
    list_rejected_items = []
    total_price_items = 0.0
    digital_value = True

    for i in range(len(list_shopping_cart_values)):
        if list_shopping_cart_values[i]["quantity_purchased"] <= list_books_values[i]["item_quantity"]:
            total_price_items += list_books_values[i]["item_price"] * list_shopping_cart_values[i]["quantity_purchased"]

            is_digital = list_books_values[i]["format"]["digital"]
            if not is_digital:
                digital_value = False
        else:
            list_shopping_cart_values[i]["quantity_purchased"] = list_books_values[i]["item_quantity"]
            list_rejected_items.append(list_shopping_cart_values[i])

    if list_rejected_items:
        return dict(status=400, books_lacking=list_rejected_items, stocks=False)
    else:
        reserve_books(list_shopping_cart_values, list_books_values)
        return dict(status=200, books_stocks=list_books_values, stocks=True, total_price=total_price_items,
                    digital=digital_value)


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


def finish_purchase(books_cart: list, success: bool) -> dict:
    list_ids = list(map(lambda x: x['_id'], books_cart))
    try:
        books_saved = book_db.search_books_by_id(*list_ids)
        for i in range(len(books_saved)):
            if success:
                if books_saved[i]["reserve_quantity"] >= books_cart[i]["quantity_purchased"]:
                    books_saved[i]["reserve_quantity"] -= books_cart[i]["quantity_purchased"]
                    book_db.update_book_db(books_saved[i])
                else:
                    return dict(
                        status=400,
                        error="Erro ao finalizar a compra.",
                        message="A quantidade de livros informada está incorreta."
                    )
            else:
                books_saved[i]["item_quantity"] += books_cart[i]["quantity_purchased"]

    except Exception as error:
        return dict(status=400, error=f"Dados incompletos: {error.args[0]}", message="Verifique os dados informados.")
    return dict(status=200, message="Compra finalizada! Estoque alterado com sucesso.")
