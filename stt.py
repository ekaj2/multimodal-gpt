import numpy as np
import sounddevice as sd
from scipy.io import wavfile
from openai import OpenAI

from settings import SILENCE_BREAK_SAMPLE_DURATION, SILENCE_BREAK_THRESHOLD, SILENCE_DURATION, SILENCE_THRESHOLD, FILES_DIR

client = OpenAI()


def listen():
    fs = 44100
    recording = []
    silence_samples = int(SILENCE_DURATION * fs)

    stream = sd.InputStream(samplerate=fs, channels=1)
    print("Listening...")
    stream.start()
    while True:
        data = stream.read(silence_samples)[0]
        recording.extend(data)
        volume_norm = np.linalg.norm(data) / np.sqrt(silence_samples)
        if volume_norm < SILENCE_THRESHOLD:
            print("Stopped")
            break
        else:
            print(".", end="", flush=True)
    stream.stop()
    recording = np.array(recording)
    wavfile.write(FILES_DIR / "output.wav", fs, recording)
    with open(FILES_DIR / "output.wav", "rb") as audio_file:
        command = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
        print(f"Processing image to answer: {command}")
    return command


def wait_for_speech():
    fs = 44100
    silence_samples = int(SILENCE_BREAK_SAMPLE_DURATION * fs)

    stream = sd.InputStream(samplerate=fs, channels=1)
    print("Listening in the background...")
    stream.start()
    while True:
        data = stream.read(silence_samples)[0]
        volume_norm = np.linalg.norm(data) / np.sqrt(silence_samples)
        if volume_norm > SILENCE_BREAK_THRESHOLD:
            print("Sound detected")
            break
        else:
            print(".", end="", flush=True)
    stream.stop()
    return True
