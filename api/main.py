from typing import Annotated
from fastapi import FastAPI, Security, Header, File, UploadFile
from fastapi.security import APIKeyHeader
# from controllers.database import db_connect
import controllers.auth as auth
from controllers.speech_to_text.transcribe import transcribe_from_file_upload
from models.user import SignUpRequestModel

app = FastAPI()
api_key_header = APIKeyHeader(name='x-api-key')


@app.get('/status')
async def status():
    return {
        'status': 'OK',
    }


# TODO: needs to use header params instead of normal params
@app.post('/register')
async def register(user_details: SignUpRequestModel):
    generated_api_key = auth.register(user_details)

    return {
        'message': 'Succesfully created new user: %s, please make a note of api key' % user_details.username,
        'api_key': generated_api_key
    }


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
