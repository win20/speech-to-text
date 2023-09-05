from transcribe import transcribe


def main():
    SPEECH_FILE = 'audio/test.wav'
    trancription = transcribe(SPEECH_FILE)

    print(trancription)


if __name__ == "__main__":
    main()
