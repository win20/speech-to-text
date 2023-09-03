import torch
import torchaudio
import IPython
import matplotlib.pyplot as plt
from greedy_ctc_decoder import GreedyCTCDecoder

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

SPEECH_FILE = 'audio/harvard.wav'
IPython.display.Audio(SPEECH_FILE)
bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H
model = bundle.get_model().to(device)

waveform, sample_rate = torchaudio.load(SPEECH_FILE)
waveform.to(device)

if sample_rate != bundle.sample_rate:
    waveform = torchaudio.functional.resample(
        waveform, sample_rate, bundle.sample_rate)

with torch.inference_mode():
    features, _ = model.extract_features(waveform)

with torch.inference_mode():
    emission, _ = model(waveform)

decoder = GreedyCTCDecoder(labels=bundle.get_labels())
transcript = decoder(emission[0])
print(transcript)
