
from pathlib import Path
from PIL import ImageGrab


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FOLDER = PROJECT_ROOT / "data"
SCREENSHOT_PATH = DATA_FOLDER / "screen_capture.png"


def capture_screen():
    DATA_FOLDER.mkdir(exist_ok=True)

    screenshot = ImageGrab.grab()

    screenshot.save(SCREENSHOT_PATH)

    print("MIRROR Screen Capture")
    print("=====================")
    print(f"Screenshot saved to:")
    print(SCREENSHOT_PATH)

    return SCREENSHOT_PATH


if __name__ == "__main__":
    capture_screen()