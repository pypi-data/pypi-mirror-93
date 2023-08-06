from http import HTTPStatus
from typing import List

from requests import Response, Session


def mk_exc(response: Response) -> RuntimeError:
    return RuntimeError(
        f"""
    Error from B2C TMS
    status: {response.status_code}
    error: {response.text}
    """
    )


def auto_paginate(
    session: Session, url: str, params: dict = None, after: str = None
) -> List[dict]:
    if not params:
        params = {}

    def _iter():
        cursor = after
        while True:
            req_params = dict(params)
            if cursor:
                req_params["after"] = cursor

            response = session.get(url, params=req_params)

            if response.status_code != HTTPStatus.OK:
                raise mk_exc(response)

            for item in response.json()["data"]:
                yield item

            cursor = response.json()["meta"]["cursor"].get("last")
            if not cursor:
                break

    return list(_iter())
