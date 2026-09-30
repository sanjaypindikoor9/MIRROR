import time

import win32gui
import win32con


class WindowsController:

    def __init__(self):
        self.preview_mode = True

    # ==============================================
    # FIND WINDOWS
    # ==============================================

    def find_windows(self):

        windows = []

        def callback(hwnd, _):

            if not win32gui.IsWindowVisible(hwnd):
                return

            title = win32gui.GetWindowText(hwnd).strip()

            if not title:
                return

            windows.append({
                "hwnd": hwnd,
                "title": title
            })

        win32gui.EnumWindows(
            callback,
            None
        )

        return windows

    # ==============================================
    # FIND WINDOW BY TITLE
    # ==============================================

    def find_window_by_title(self, title):

        title_lower = title.lower()

        for window in self.find_windows():

            if title_lower in window["title"].lower():

                return window["hwnd"]

        return None

    # ==============================================
    # RESTORE WINDOW
    # ==============================================

    def restore_window(self, hwnd):

        if self.preview_mode:

            print(
                "[PREVIEW] Would restore window."
            )

            return

        win32gui.ShowWindow(
            hwnd,
            win32con.SW_RESTORE
        )

        time.sleep(0.2)

        win32gui.SetForegroundWindow(hwnd)

    # ==============================================
    # MINIMIZE WINDOW
    # ==============================================

    def minimize_window(self, hwnd):

        if self.preview_mode:

            print(
                "[PREVIEW] Would minimize window."
            )

            return

        win32gui.ShowWindow(
            hwnd,
            win32con.SW_MINIMIZE
        )

    # ==============================================
    # TEST TARGET
    # ==============================================

    def test_target(self, title):

        print(
            "\nMIRROR WINDOW TARGET TEST"
        )

        print(
            "========================="
        )

        print(
            f"\nSearching for:"
        )

        print(
            f"  {title}"
        )

        hwnd = self.find_window_by_title(title)

        if hwnd is None:

            print(
                "\n✕ Window not found."
            )

            return

        print(
            "\n✓ Window found."
        )

        print(
            f"  HWND: {hwnd}"
        )

        print(
            "\nTesting restore action..."
        )

        self.restore_window(hwnd)

        print(
            "\nTesting minimize action..."
        )

        self.minimize_window(hwnd)

        print(
            "\nNo actual changes made."
        )


# ==============================================
# TEST
# ==============================================

if __name__ == "__main__":

    controller = WindowsController()

    controller.test_target(
        "Greeting Nova"
    )