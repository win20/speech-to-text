import torch
import torchaudio
import IPython
import matplotlib.pyplot as plt
from greedy_ctc_decoder import GreedyCTCDecoder


def extract_waveform(bundle, device, speech_file):
    bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H

    waveform, sample_rate = torchaudio.load(speech_file)
    waveform.to(device)

    if (sample_rate != bundle.sample_rate):
        waveform = torchaudio.functional.resample(
            waveform, sample_rate, bundle.sample_rate)

    return waveform


def extract_accoustic_features(model, waveform):
    with torch.inference_mode():
        features, _ = model.extract_features(waveform)

    return features


def classify_features(model, waveform):
    with torch.inference_mode():
        emission, _ = model(waveform)

    return emission


def transcribe(speech_file):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H
    model = bundle.get_model().to(device)

    waveform = extract_waveform(bundle, device, speech_file)
    features = extract_accoustic_features(model, waveform)
    print(features)

    emission = classify_features(model, waveform)

    decoder = GreedyCTCDecoder(labels=bundle.get_labels())
    transcript = decoder(emission[0])

    return transcript


def main():
    SPEECH_FILE = 'audio/speech_sample.ogg'
    trancription = transcribe(SPEECH_FILE)

    print(trancription)


if __name__ == "__main__":
    main()
