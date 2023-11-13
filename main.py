from openai import OpenAI

from screenshot import take_screenshot
from stt import listen, wait_for_speech
from tts import say
from image_api import submit_image
from settings import FILES_DIR

client = OpenAI()

while True:
    say("Hi I'm your personal assistant. Just start talking if you need anything!")
    wait_for_speech()

    image_path = FILES_DIR / "screenshot.png"
    screenshot = take_screenshot(image_path)

    say("Please ask a question or give a command.")
    command = listen()

    gpt_result = submit_image(
        prompt=f"{command}",
        image_path=image_path
    )

    if gpt_result is not None:
        print("-" * 80)
        content = gpt_result["choices"][0]["message"]["content"]
        print(content)
        say(content)
