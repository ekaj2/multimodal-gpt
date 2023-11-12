import subprocess
import pyautogui
import pywinctl as pwc


def take_screenshot(output_path):

    all_windows = pwc.getAllWindows()
    input_str = "Which window would you like to look at?\n"
    i = 1
    for title in [a.title for a in all_windows]:
        input_str += f"{i}: {title}\n"
        i += 1
    win = all_windows[int(input(input_str+"> ")) - 1]

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
