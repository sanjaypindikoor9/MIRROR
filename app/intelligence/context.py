def classify_application(process, title=""):
    process = process.lower()
    title = title.lower()

    # Development
    if any(x in process for x in ["code.exe", "pycharm", "devenv.exe"]):
        return "Development"

    # Web browsing
    if any(x in process for x in ["msedge.exe", "chrome.exe", "firefox.exe"]):
        return "Research / Browsing"

    # Communication
    if any(x in process for x in ["whatsapp", "discord", "teams", "slack"]):
        return "Communication"

    # Documents / PDFs
    if any(x in process for x in ["acrobat", "sumatrapdf"]):
        return "Reference"

    # File management
    if process == "explorer.exe":
        return "File Management"

    # ChatGPT
    if "chatgpt" in process or "chatgpt" in title:
        return "AI Assistant"

    return "Other"


if __name__ == "__main__":
    tests = [
        ("Code.exe", "activity.py"),
        ("msedge.exe", "Google"),
        ("explorer.exe", ""),
        ("ChatGPT Classic.exe", "Greeting Nova"),
    ]

    for process, title in tests:
        category = classify_application(process, title)
        print(f"{process} → {category}")