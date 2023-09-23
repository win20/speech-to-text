from fastapi import Depends, FastAPI, HTTPException, Security, Header
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Annotated, List
import MySQLdb


# from speech_to_text.transcribe import transcribe

db_config = {
    'host': 'localhost',
    'user': 'root',
    'passwd': 'Candi.201099',
    'db': 'scribe',
}
conn = MySQLdb.connect(**db_config)


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
api_key_header = APIKeyHeader(name='x-api-key')


def authenticate(
    api_key_header: str = Security(api_key_header),
    username: Annotated[str | None, Header()] = None,
    password: Annotated[str | None, Header()] = None
) -> List[str]:
    cursor = conn.cursor()

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


@app.get('/protected')
async def protected_route(
    test: str = Security(authenticate),
):
    return {'message': 'hello from protected'}


@app.get('/status')
async def status():
    return {
        'message': 'OK, server up and running.'
    }


@app.get('/transcribe')
async def root():
    SPEECH_FILE = '../audio/test.wav'
    trancription = transcribe(SPEECH_FILE)

    return {
        'message': trancription
    }
