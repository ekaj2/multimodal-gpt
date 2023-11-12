# A Screenshot-based Multimodal GPT Assistant

1. Python `sounddevice` for recording audio until you stop speaking
1. Whisper API for transcribing audio
1. OpenAI TTS for speech
1. PyWinCtl and pyautogui for screenshots of a specific window
1. OpenAI Vision API to process the screenshot and answer your prompt

## Installation

```bash
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Configuration

All project-wide settings are in settings.py.
