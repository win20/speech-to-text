from fastapi import FastAPI
from transcribe import transcribe

app = FastAPI()


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
