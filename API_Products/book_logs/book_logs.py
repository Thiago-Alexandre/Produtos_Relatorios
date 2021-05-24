from datetime import datetime

from flask import Request

from database.auth import KEYS
from database.book_db import get_books_by_id


def generate_log_data(request: Request, response_data: dict) -> dict:
    body_request = request.json
    status = response_data["status"]

    if "Access-Key" in list(request.headers.keys()):
        access_key = request.headers.get("Access-Key")
        user = list(KEYS.keys())[list(KEYS.values()).index(access_key)]
    else:
        user = "Other"

    log_data = dict(
        ocurrence_datetime=datetime.now().isoformat(sep=" "),
        client_ip=request.remote_addr,
        user=user,
        path=request.path,
        method=request.method,
        status=status,
        body_request=body_request
    )

    if status == 200:
        log_data.pop("body_request")

    book_is_present = "book" in list(response_data.keys())

    if request.path == "/books/purchase/finish" or request.path == "/books/stock/verify":
        if "books" in list(response_data.keys()):
            log_data["before"] = response_data["books"]
            log_data["after"] = get_books_by_id(
                *[bk["_id"] for bk in response_data["books"]],
                _id=1, item_quantity=1, reserve_quantity=1,
            )

    elif request.method == "POST":
        if book_is_present:
            log_data["inserted"] = response_data["book"]

    elif request.method == "PUT":
        if book_is_present:
            log_data["before"] = response_data["book"]
            log_data["after"] = {key: body_request[key] for key in list(response_data["book"].keys())}

    elif request.method == "DELETE":
        if book_is_present:
            log_data["deleted"] = response_data["book"]

    if "error" in list(response_data.keys()):
        log_data["error"] = response_data["error"]

    if "message" in list(response_data.keys()):
        log_data["message"] = response_data["message"]

    return log_data
