from pathlib import Path
BASE_DIR = Path(__file__).parent
FILES_DIR = BASE_DIR / "files"

# region USER-CUSTOMIZABLE SETTINGS

# the volume threshold to consider silent
SILENCE_THRESHOLD = 0.025
# how long to wait during silence before stopping the recording
SILENCE_DURATION = 2

# endregion
