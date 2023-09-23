from fastapi import FastAPI, Security, Header
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


@app.get('/transcribe')
async def root():
    SPEECH_FILE = '../audio/test.wav'
    trancription = transcribe(SPEECH_FILE)

    return {
        'message': trancription
    }
