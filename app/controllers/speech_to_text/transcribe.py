import torch
import torchaudio
import matplotlib.pyplot as plt
from .greedy_ctc_decoder import GreedyCTCDecoder
from pydub import AudioSegment
import os
import aiofiles
from fastapi import UploadFile, File


def extract_waveform(bundle, device, speech_file: str) -> torch.Tensor:
    """Extract waveforme and sample rate from file

    Args:
        bundle (Wav2Vec2ASRBundle): bundle for pretrained model
        device (device): cpu or cuda
        speech_file (str): path to speech file

    Returns:
        array: waveforms extracted
    """
    bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H

    waveform, sample_rate = torchaudio.load(speech_file)
    waveform.to(device)

    if (sample_rate != bundle.sample_rate):
        waveform = torchaudio.functional.resample(
            waveform, sample_rate, bundle.sample_rate)

    return waveform


def extract_accoustic_features(model, waveform: torch.Tensor) -> torch.Tensor:
    with torch.inference_mode():
        features, _ = model.extract_features(waveform)

    return features


def classify_features(model, waveform: torch.Tensor) -> torch.Tensor:
    with torch.inference_mode():
        emission, _ = model(waveform)

    return emission


def speech_to_text(speech_file: str) -> str:
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H
    model = bundle.get_model().to(device)

    waveform = extract_waveform(bundle, device, speech_file)
    features = extract_accoustic_features(model, waveform)

    emission = classify_features(model, waveform)

    decoder = GreedyCTCDecoder(labels=bundle.get_labels())
    text = decoder(emission[0])

    return text


def convert_to_wav(file: str, destination: str) -> None:
    audio = AudioSegment.from_file(file)
    audio.export(destination, format='wav')

    os.remove(file)


def transcribe(speech_file: str) -> str:
    file_root, file_extension = os.path.splitext(speech_file)

    if file_extension == '.mp3':
        convert_to_wav(speech_file, file_root + '.wav')

    text = speech_to_text(speech_file)
    text = text.replace('|', ' ').lower()

    model, example_texts, languages, punct, apply_te = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                                                      model='silero_te')
    transcription = apply_te(text, lan='en')

    return transcription


async def transcribe_from_file_upload(file: UploadFile) -> str:
    out_file_path = './audio/audio.wav'

    async with aiofiles.open(out_file_path, 'wb') as out_file:
        while content := await file.read(1024):
            await out_file.write(content)

    return transcribe(out_file_path)
