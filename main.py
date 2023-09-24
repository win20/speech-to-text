import aiofiles
from typing import Annotated
from fastapi import FastAPI, Security, Header, File, UploadFile
from fastapi.security import APIKeyHeader
from database import db_connect
from controllers.auth import authenticate
from controllers.speech_to_text.transcribe import transcribe


app = FastAPI()
api_key_header = APIKeyHeader(name='x-api-key')
db = db_connect()


@app.get('/status')
async def status():
    return {
        'message': 'OK, server up and running.'
    }


@app.get('/protected')
async def protected_route(
    _: str = Security(authenticate),
):
    test = 'test'
    return {'message': test}


@app.post('/transcribe')
async def root(file: UploadFile = File(...), _: str = Security(authenticate)):
    out_file_path = './audio/audio.wav'

    async with aiofiles.open(out_file_path, 'wb') as out_file:
        while content := await file.read(1024):
            await out_file.write(content)

    transcription = transcribe(out_file_path)

    return {
        'message': transcription
    }
