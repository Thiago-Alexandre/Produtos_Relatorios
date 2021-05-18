from datetime import datetime

from flask import Request

from database.auth import KEYS


def generate_log_data(request: Request, response: dict) -> dict:
    if "Access-Key" in list(request.headers.keys()):
        access_key = request.headers.get("Access-Key")
        user = list(KEYS.keys())[list(KEYS.values()).index(access_key)]
    else:
        # user = "Anonymous"
        user = "Other"

    log_data = dict(
        ocurrence_datetime=datetime.now().isoformat(sep=" "),
        client_ip=request.remote_addr,
        user=user,
        path=request.path,
        method=request.method,
        body_request=dict(request.json),
        status=response['status']
    )
    if "error" in list(response.keys()):
        log_data["error"] = response["error"]

    if "message" in list(response.keys()):
        log_data["message"] = response["message"]

    return log_data
