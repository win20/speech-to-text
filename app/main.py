import aiofiles
from typing import Annotated
from fastapi import FastAPI, Security, Header, File, UploadFile
from fastapi.security import APIKeyHeader
from app.database import db_connect
from app.controllers.auth import authenticate
from app.controllers.speech_to_text.transcribe import transcribe_from_file_upload

app = FastAPI()
api_key_header = APIKeyHeader(name='x-api-key')
db = db_connect()


@app.get('/status')
async def status():
    return {
        'message': 'OK, server up and running.'
    }


@app.get('/status-protected')
async def protected_route(
    _: str = Security(authenticate),
):
    return {'message': 'OK, authentification successful'}


@app.post('/transcribe')
async def root(file: UploadFile = File(...), _: str = Security(authenticate)):
    transcription = await transcribe_from_file_upload(file)

    return {
        'message': transcription
    }
