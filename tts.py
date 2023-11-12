from pathlib import Path
import subprocess
from openai import OpenAI

client = OpenAI()
BASE_DIR = Path(__file__).parent
FILES_DIR = BASE_DIR / "files"


def say(text):
    speech_file_path = FILES_DIR / "speech.mp3"
    response = client.audio.speech.create(
        model="tts-1-hd",
        voice="alloy",
        input=text
    )
    response.stream_to_file(speech_file_path)

    # play the output
    subprocess.run(["afplay", speech_file_path])
