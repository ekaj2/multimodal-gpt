import subprocess
import pyautogui
import pywinctl as pwc
from string import punctuation

from stt import listen
from tts import say


def strip_punc(text):
    return "".join([c for c in text if c not in punctuation])


def word_to_num(text):
    """Try to find a single digit number in the text"""

    words = text.split()
    numbers = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
    }
    for word in words:
        stripped_word = strip_punc(word.strip().lower())
        if stripped_word in numbers.keys():
            return numbers[stripped_word]
    return None


def take_screenshot(output_path):

    all_windows = pwc.getAllWindows()
    input_str = "Please choose a window:\n"
    i = 1
    for title in [a.title for a in all_windows]:
        input_str += f"{i}: {title}\n"
        i += 1

    say(input_str)
    while True:
        transcript = listen()
        num = word_to_num(transcript)
        if num is None:
            say("Please choose a number...")
        else:
            break

    win = all_windows[num - 1]
    print(f"Taking a screenshot of: {win.title}")

    x = win.position.x
    y = win.position.y
    width = win.width
    height = win.height

    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    screenshot.save(output_path)


if __name__ == "__main__":
    take_screenshot("screenshot.png")
    # call os "open screenshot.png"
    subprocess.call(["open", "screenshot.png"])
