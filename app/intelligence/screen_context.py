from app.capture.screen import capture_screen
from app.perception.ocr import extract_text
from app.intelligence.context import classify_application


def analyze_screen(process, title):
    """
    Combine application information with OCR text
    to create a basic screen context.
    """

    # Capture current screen
    capture_screen()

    # Extract visible text
    screen_text = extract_text()

    # Classify the active application
    application_context = classify_application(
        process,
        title
    )

    return {
        "process": process,
        "title": title,
        "application_context": application_context,
        "screen_text": screen_text
    }


if __name__ == "__main__":

    result = analyze_screen(
        "Code.exe",
        "MIRROR - Visual Studio Code"
    )

    print("\nMIRROR SCREEN CONTEXT")
    print("=====================")

    print(
        f'Application: {result["process"]}'
    )

    print(
        f'Title: {result["title"]}'
    )

    print(
        f'Context: {result["application_context"]}'
    )

    print("\nVisible screen text:")
    print("--------------------")
    print(result["screen_text"])