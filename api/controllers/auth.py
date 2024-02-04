from fastapi import Depends, FastAPI, HTTPException, Security, Header
from fastapi.security import APIKeyHeader
from typing import Annotated, List
from .database import query_get

api_key_header = APIKeyHeader(name='x-api-key')


def register(username: str, password: str):
    user = query_get("""
        SELECT id, consumer
        FROM consumer
        WHERE consumer = %s
    """, (username))

    if len(user) != 0:
        raise HTTPException(
            status_code=409,
            detail='Username already exists'
        )


def authenticate(
    api_key_header: str = Security(api_key_header),
    username: Annotated[str | None, Header()] = None,
    password: Annotated[str | None, Header()] = None
) -> List[str]:
    user_info = get_user_info_by_username(username)

    if (
        len(user_info) == 0 or
        password != user_info[0]['password'] or
        api_key_header != user_info[0]['api_key']
    ):
        raise HTTPException(status_code=401, detail='Invalid details received')


def get_user_info_by_username(username: str) -> list:
    result = query_get("""
        SELECT password, api_key
        FROM scribe.consumer
        WHERE consumer = %s;
    """, username)

    return result