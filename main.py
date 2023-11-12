from openai import OpenAI

from screenshot import take_screenshot
from stt import listen
from tts import say
from image_api import submit_image
from settings import FILES_DIR

client = OpenAI()

image_path = FILES_DIR / "screenshot.png"
screenshot = take_screenshot(image_path)

say("Hi I'm your personal assistant. How can I help you?")
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
