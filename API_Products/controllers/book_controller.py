from controllers.utils import validate_book
from database.book_db import get_books_by_id, insert_book_db, read_all_books_db, update_book_db


def insert_book(dict_values: dict) -> dict:
    """
    Get a dictionary with book data and insert in db.
    :param dict_values: a dict with book data.
    :return:            a dict with response of request.
    """
    try:
        validate_book(dict_values)
    except Exception as error:
        return dict(status=400, error=error.args[0], message=error.args[1])

    try:
        dict_values["reserve_quantity"] = 0
        dict_values["rating"] = 0

        inserted_book = insert_book_db(dict_values)
        inserted_book["_id"] = str(inserted_book["_id"])

        return dict(status=200, message="Livro cadastrado com sucesso!", book=inserted_book)
    except Exception as error:
        return dict(status=500, error=error.args[0], message=error.args[1])


def update_book(dict_values: dict) -> dict:
    """
    Gets a dictionary with book data and update this data in db.
    :param dict_values: a dict with book data.
    :return:            a dict with response of request including book before update.
    """
    try:

        validate_book(dict_values, is_update=True)
    except Exception as error:
        return dict(status=400, error=error.args[0], message=error.args[1])

    try:
        updated_book = update_book_db(dict_values)[0]
        updated_book["_id"] = str(updated_book["_id"])

        return dict(status=200, message="Livro atualizado com sucesso!", book=updated_book)
    except Exception as error:
        return dict(status=500, error=error.args[0], message=error.args[1])


def get_book_list() -> dict:
    """
    Gets a book list in data base and returns these items in a list of dictionaries.
    :return:    a list of dictionaries with the books data.
    """
    try:
        result_data = read_all_books_db()

        if result_data:
            return dict(status=200, result_data=result_data)
        else:
            return dict(status=200, message="Nenhum livro cadastrado.", result_data=[])
    except Exception as error:
        return dict(status=500, error=error.args[0], message="Tente novamente mais tarde.")


def check_stock(shopping_cart: list) -> dict:
    """
    This function get a shopping cart with books, checks these items is available in stock and withdraw the item
    quantity required.
    :param shopping_cart:   a list with book dictionaries of shopping cart.
    :return:                a dict with response of request.
    """

    list_ids = list(map(lambda x: x["item_id"], shopping_cart))
    try:
        book_list_db = get_books_by_id(*list_ids)
    except Exception as err:
        return dict(status=400, error=err.args[0], message="Verifique os dados informados.")

    no_stock_items = []
    total_price_car = 0.0
    contains_digital_books = True

    for book_db, book_cart in zip(book_list_db, shopping_cart):

        quantity_purchased = book_cart["quantity_purchased"]
        item_quantity = book_db["item_quantity"]
        item_price = book_db["item_price"]
        is_digital = book_db["format"]["digital"]

        total_price_car += item_price * quantity_purchased

        if quantity_purchased <= item_quantity:
            if not is_digital:
                contains_digital_books = False

            book_db["item_quantity"] -= quantity_purchased
            book_db["reserve_quantity"] += quantity_purchased

        else:
            book_cart["quantity_purchased"] = item_quantity
            no_stock_items.append(book_cart)

    if no_stock_items:
        return dict(status=400, books_lacking=no_stock_items, stocks=False)
    else:
        try:
            books_updated_successfully = update_book_db(book_list_db)
            return dict(status=200, books_stocks=book_list_db, stocks=True, total_price=total_price_car,
                        digital=contains_digital_books, books=books_updated_successfully)
        except Exception as err:
            return dict(status=500, error=err.args[0], message="Não foi possível reservar produtos do estoque.")


def finish_purchase(shopping_cart: list, success: bool) -> dict:
    """
    This function get a shopping cart with books and withdraw the items quantity purchased in db if success is True. If
    success is false, he returns the items to the stock in db.
    :param shopping_cart:   a list with book dictionaries of shopping cart.
    :param success:         True if purchase is sucessfully.
    :return:                a dict with response of request.
    """

    list_ids = list(map(lambda x: x["item_id"], shopping_cart))
    try:
        book_list_db = get_books_by_id(*list_ids)
    except Exception as err:
        return dict(status=400, error=err.args[0], message="Verifique os dados informados.")

    updated_book_list = []
    if success:
        response_message = "Compra finalizada! Estoque alterado com sucesso."
        for book_db, book_cart in zip(book_list_db, shopping_cart):
            if book_db["reserve_quantity"] >= book_cart["quantity_purchased"]:
                updated_book_list.append({
                    "_id": book_db.get("_id"),
                    "item_quantity": book_db["item_quantity"],
                    "reserve_quantity": book_db["reserve_quantity"] - book_cart["quantity_purchased"]
                })
            else:
                return dict(
                    status=400,
                    error="Erro ao finalizar a compra.",
                    message="A quantidade de livros informada está incorreta."
                )
    else:
        response_message = "Compra não finalizada! Produtos devolvidos ao estoque."

        for book_db, book_cart in zip(book_list_db, shopping_cart):

            if 0 < book_cart["quantity_purchased"] <= book_db["reserve_quantity"]:
                updated_book_list.append({
                    "_id": book_db.get("_id"),
                    "item_quantity": book_db["item_quantity"] + book_cart["quantity_purchased"],
                    "reserve_quantity": book_db["reserve_quantity"] - book_cart["quantity_purchased"]
                })
            else:
                return dict(
                    status=400,
                    error="Erro ao devolver livros ao estoque.",
                    message="A quantidade de livros informada está incorreta."
                )

    try:
        books_updated_sucessfully = update_book_db(updated_book_list)
        if books_updated_sucessfully:
            return dict(status=200, message=response_message, books=books_updated_sucessfully)
        else:
            return dict(
                status=500,
                error="Não foi possível atualizar os dados dos livros.",
                message="Compra não finalizada"
            )
    except Exception as err:
        return dict(status=500, error=err, message="Compra não finalizada.")
