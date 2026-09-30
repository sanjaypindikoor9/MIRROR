from pathlib import Path

import pytesseract
from PIL import Image


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCREENSHOT_PATH = PROJECT_ROOT / "data" / "screen_capture.png"


def extract_text():

    if not SCREENSHOT_PATH.exists():
        print("Screenshot not found.")
        return ""

    image = Image.open(SCREENSHOT_PATH)

    # Convert to grayscale to improve OCR
    image = image.convert("L")

    # OCR configuration
    config = "--psm 6"

    text = pytesseract.image_to_string(
        image,
        config=config
    )

    lines = []

    for line in text.splitlines():

        line = line.strip()

        if len(line) >= 4:
            lines.append(line)

    cleaned_text = "\n".join(lines)

    print("\nMIRROR SCREEN UNDERSTANDING")
    print("===========================")

    if cleaned_text:
        print(cleaned_text)
    else:
        print("No useful text detected.")

    return cleaned_text


if __name__ == "__main__":
    extract_text()