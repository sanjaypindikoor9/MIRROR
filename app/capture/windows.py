import win32gui
import win32process
import psutil


def get_open_windows():
    windows = []

    def callback(hwnd, _):
        if not win32gui.IsWindowVisible(hwnd):
            return

        title = win32gui.GetWindowText(hwnd).strip()

        if not title:
            return

        try:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)

            windows.append({
                "hwnd": hwnd,
                "title": title,
                "process": process.name(),
                "pid": pid
            })

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    win32gui.EnumWindows(callback, None)

    return windows


if __name__ == "__main__":
    for window in get_open_windows():
        print(
            f'{window["process"]}  |  {window["title"]}'
        )