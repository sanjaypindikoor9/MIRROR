import time

import win32gui
import win32process
import psutil

from app.storage.database import initialize_database, save_activity
from app.intelligence.context import classify_application


def get_active_window():
    hwnd = win32gui.GetForegroundWindow()

    if not hwnd:
        return None

    title = win32gui.GetWindowText(hwnd).strip()

    try:
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process = psutil.Process(pid)

        return {
            "title": title,
            "process": process.name(),
            "pid": pid
        }

    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return None


def track_activity():
    previous_process = None

    print("MIRROR Activity Tracker")
    print("========================")
    print("Monitoring application switches...")
    print("Activity will be saved to mirror.db")
    print("Press Ctrl+C to stop.\n")

    while True:
        window = get_active_window()

        if window:
            current_process = window["process"]

            if current_process != previous_process:

                context = classify_application(
                    window["process"],
                    window["title"]
                )

                print(
                    f'→ {window["process"]} | '
                    f'{context} | '
                    f'{window["title"]}'
                )

                save_activity(
                    window["process"],
                    window["title"],
                    window["pid"]
                )

                previous_process = current_process

        time.sleep(1)


if __name__ == "__main__":
    initialize_database()

    try:
        track_activity()
    except KeyboardInterrupt:
        print("\nMIRROR tracker stopped.")