import numpy as np
import sounddevice as sd
from scipy.io import wavfile
from pathlib import Path
from openai import OpenAI

client = OpenAI()

BASE_DIR = Path(__file__).parent
FILES_DIR = BASE_DIR / "files"


def listen():
    fs = 44100
    recording = []
    silence_threshold = 0.025
    silence_duration = 2
    silence_samples = int(silence_duration * fs)

    stream = sd.InputStream(samplerate=fs, channels=1)
    print("Listening...")
    stream.start()
    while True:
        data = stream.read(silence_samples)[0]
        recording.extend(data)
        volume_norm = np.linalg.norm(data) / np.sqrt(silence_samples)
        if volume_norm < silence_threshold:
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
