from openai import OpenAI

from screenshot import take_screenshot
from stt import listen, wait_for_speech
from tts import say
from image_api import submit_image
from settings import FILES_DIR

client = OpenAI()

say("Hi I'm your personal assistant. Just start talking if you need anything!")
while True:
    wait_for_speech()

    image_path = FILES_DIR / "screenshot.png"
    screenshot = take_screenshot(image_path)

    say("Please ask a question or give a command.")
    command = listen(minimum_length=3000)

    gpt_result = submit_image(
        prompt=f"{command}",
        image_path=image_path
    )

    if gpt_result is not None:
        print("-" * 80)
        content = ""
        try:
            content = gpt_result["choices"][0]["message"]["content"]
            print(content)
            say(content, confirm_before_speaking=True)
        except KeyError as e:
            print(e)
            print(gpt_result)
            say(
                f"Unfortunately we ran into an issue. Please try again later. Here's the issue description: {e}")
    say("Let me know if you need anything else.")
