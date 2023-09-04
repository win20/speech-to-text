from transcribe import transcribe


def main():
    SPEECH_FILE = 'audio/281047.mp3'
    trancription = transcribe(SPEECH_FILE)

    print(trancription)


if __name__ == "__main__":
    main()
