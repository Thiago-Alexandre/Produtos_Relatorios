from datetime import datetime

from flask import Request

from database.auth import KEYS


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

    log_data.pop("body_request")

    book_is_present = "book" in list(response_data.keys())

    if request.method == "POST":
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
