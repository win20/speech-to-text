import secrets
from fastapi import Depends, FastAPI, HTTPException, Security, Header
from fastapi.security import APIKeyHeader
from typing import Annotated, List
from models.user import SignUpRequestModel
from .database import query_get, query_put

api_key_header = APIKeyHeader(name='x-api-key')


def register(user_model: SignUpRequestModel) -> str:
    result = get_user_info_by_username(user_model.username)

    if len(result) != 0:
        raise HTTPException(
            status_code=409,
            detail='Username already exists'
        )

    api_key = secrets.token_urlsafe(16)

    query_put("""
        INSERT INTO consumer (consumer, password, api_key)
        VALUES (%s, %s, %s)
    """, (user_model.username, user_model.password, api_key))

    return api_key


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