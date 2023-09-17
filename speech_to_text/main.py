from fastapi import FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader
from transcribe import transcribe

app = FastAPI()
api_key_header = APIKeyHeader(name='X-API-Key')

# TODO: testing... need to create key in database
api_keys = [
    "my_api_key"
]


def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header in api_keys:
        return api_key_header

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid or missing API key'
    )


@app.get('/protected')
async def protected_route(api_key: str = Security(get_api_key)):
    return {'message': 'Access granted'}


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


# def main():
#     SPEECH_FILE = 'audio/test.wav'
#     trancription = transcribe(SPEECH_FILE)

#     print(trancription)

#     # print('Hello from transcribe script')


# if __name__ == "__main__":
#     main()
