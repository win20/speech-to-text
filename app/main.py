import aiofiles
from typing import Annotated
from fastapi import FastAPI, Security, Header, File, UploadFile
from fastapi.security import APIKeyHeader
from controllers.database import db_connect
import controllers.auth as auth
from controllers.speech_to_text.transcribe import transcribe_from_file_upload

app = FastAPI()
api_key_header = APIKeyHeader(name='x-api-key')
db = db_connect()


@app.get('/status')
async def status():
    cursor = db.cursor()
    cursor.execute('select @@version')
    output = cursor.fetchall()
    return {
        'message': output
    }


@app.post('/register')
async def register(username: str, password: str):
    auth.register(username, password)

    return {'message': 'OK'}


@app.get('/status-protected')
async def protected_route(
    _: str = Security(auth.authenticate),
):
    return {'message': 'OK, authentification successful'}


@app.post('/transcribe')
async def root(file: UploadFile = File(...), _: str = Security(auth.authenticate)):
    transcription = await transcribe_from_file_upload(file)

    return {
        'message': transcription
    }
