from fastapi import Depends, FastAPI, HTTPException, Security, Header
from fastapi.security import APIKeyHeader
from typing import Annotated, List
from .database import db_connect

api_key_header = APIKeyHeader(name='x-api-key')
db = db_connect()


def authenticate(
    api_key_header: str = Security(api_key_header),
    username: Annotated[str | None, Header()] = None,
    password: Annotated[str | None, Header()] = None
) -> List[str]:
    cursor = db.cursor()

    query = """
        SELECT password, api_key
        FROM scribe.users
        WHERE consumer = '%s';
    """ % username

    cursor.execute(query)

    data = cursor.fetchone()

    if data is None:
        raise HTTPException(
            status_code=404,
            detail='Invalid or missing username'
        )

    if data[0] == password and data[1] == api_key_header:
        return data

    raise HTTPException(
        status_code=403,
        detail='Invalid/missing API key or password'
    )