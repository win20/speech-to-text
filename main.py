from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Annotated
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


def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    cursor = conn.cursor()
    query = "SELECT id FROM scribe.users WHERE api_key = '%s'" % api_key_header
    cursor.execute(query)

    data = cursor.fetchone()

    if data is not None:
        return api_key_header

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid or missing API key'
    )


@app.get('/protected')
async def protected_route(_: str = Security(get_api_key)):
    cursor = conn.cursor()
    query = 'SELECT api_key FROM scribe.users WHERE id=1'
    cursor.execute(query)
    item = cursor.fetchone()

    cursor.close()
    return {'message': item}


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
