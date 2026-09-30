from app.storage.database import get_recent_activity
from app.intelligence.context import classify_application
from app.intelligence.task_understanding import understand_workspace
from app.planner.windows_controller import WindowsController


class WorkspaceActionEngine:

    def __init__(self):

        self.preview_mode = True

        self.window_controller = (
            WindowsController()
        )

        self.window_controller.preview_mode = (
            self.preview_mode
        )

    # ==============================================
    # CREATE WORKSPACE PLAN
    # ==============================================

    def create_plan(self, limit=50):

        activities = get_recent_activity(limit)
        workspace = understand_workspace(limit)

        if not activities or not workspace:
            return None

        primary_context = workspace[
            "primary_context"
        ]

        keep = []
        reference = []
        defer = []

        seen = set()

        distraction_words = [
            "instagram",
            "facebook",
            "netflix",
            "reddit",
            "twitter",
            "x.com"
        ]

        for activity in activities:

            process = activity["process"]

            title = (
                activity["title"]
                or process
            )

            key = (
                process,
                title
            )

            if key in seen:
                continue

            seen.add(key)

            context = classify_application(
                process,
                title
            )

            title_lower = title.lower()

            # --------------------------------------
            # EXPLICIT DISTRACTIONS
            # --------------------------------------

            if any(
                word in title_lower
                for word in distraction_words
            ):

                defer.append({
                    "process": process,
                    "title": title,
                    "reason": "Distraction detected",
                    "action": "minimize"
                })

                continue

            # --------------------------------------
            # DEVELOPMENT WORKSPACE
            # --------------------------------------

            if primary_context == "Development":

                if context == "Development":

                    keep.append({
                        "process": process,
                        "title": title,
                        "reason":
                            "Primary development task",
                        "action": "restore"
                    })

                elif context == "File Management":

                    reference.append({
                        "process": process,
                        "title": title,
                        "reason":
                            "Project files and datasets",
                        "action": "restore"
                    })

                elif context == "AI Assistant":

                    reference.append({
                        "process": process,
                        "title": title,
                        "reason":
                            "AI assistance",
                        "action": "restore"
                    })

                elif context in [
                    "Research / Browsing",
                    "Reference"
                ]:

                    reference.append({
                        "process": process,
                        "title": title,
                        "reason":
                            "Potential technical reference",
                        "action": "restore"
                    })

                else:

                    defer.append({
                        "process": process,
                        "title": title,
                        "reason":
                            "Not related to current task",
                        "action": "minimize"
                    })

            # --------------------------------------
            # OTHER TASK TYPES
            # --------------------------------------

            else:

                if context == primary_context:

                    keep.append({
                        "process": process,
                        "title": title,
                        "reason":
                            "Matches primary task context",
                        "action": "restore"
                    })

                elif context in [
                    "Research / Browsing",
                    "Reference",
                    "AI Assistant",
                    "File Management"
                ]:

                    reference.append({
                        "process": process,
                        "title": title,
                        "reason":
                            "Potential supporting context",
                        "action": "restore"
                    })

                else:

                    defer.append({
                        "process": process,
                        "title": title,
                        "reason":
                            "Not related to current task",
                        "action": "minimize"
                    })

        return {
            "task": workspace["current_task"],
            "primary_context": primary_context,
            "keep": keep,
            "reference": reference,
            "defer": defer
        }

    # ==============================================
    # APPLY WORKSPACE PLAN
    # ==============================================

    def apply_plan(self, plan):

        if not plan:

            print(
                "No workspace plan available."
            )

            return

        print(
            "\nMIRROR WORKSPACE ACTIONS"
        )

        print(
            "========================"
        )

        print(
            f'\nTask: {plan["task"]}'
        )

        # ------------------------------------------
        # KEEP
        # ------------------------------------------

        for item in plan["keep"]:

            self.execute_action(
                item,
                "restore"
            )

        # ------------------------------------------
        # REFERENCE
        # ------------------------------------------

        for item in plan["reference"]:

            self.execute_action(
                item,
                "restore"
            )

        # ------------------------------------------
        # DEFER
        # ------------------------------------------

        for item in plan["defer"]:

            self.execute_action(
                item,
                "minimize"
            )

        print(
            "\nWorkspace action pass complete."
        )

    # ==============================================
    # EXECUTE SINGLE ACTION
    # ==============================================

    def execute_action(
        self,
        item,
        action
    ):

        title = item["title"]

        print(
            f"\n[{action.upper()}]"
        )

        print(
            f"  {title}"
        )

        hwnd = (
            self.window_controller
            .find_window_by_title(title)
        )

        if hwnd is None:

            print(
                "  ✕ Window not found."
            )

            return

        print(
            f"  ✓ Window found "
            f"(HWND: {hwnd})"
        )

        if action == "restore":

            self.window_controller.restore_window(
                hwnd
            )

        elif action == "minimize":

            self.window_controller.minimize_window(
                hwnd
            )

    # ==============================================
    # PREVIEW
    # ==============================================

    def preview(self):

        plan = self.create_plan()

        if not plan:

            print(
                "Unable to create workspace plan."
            )

            return

        print(
            "\nMIRROR WORKSPACE ACTION ENGINE"
        )

        print(
            "=============================="
        )

        print(
            f'\nTask: {plan["task"]}'
        )

        print(
            f'Primary Context: '
            f'{plan["primary_context"]}'
        )

        print("\nKEEP")
        print("----")

        for item in plan["keep"]:

            print(
                f'  ✓ {item["title"]}'
            )

            print(
                f'    Action: {item["action"]}'
            )

        if not plan["keep"]:

            print("  None")

        print("\nREFERENCE")
        print("---------")

        for item in plan["reference"]:

            print(
                f'  → {item["title"]}'
            )

            print(
                f'    Action: {item["action"]}'
            )

        if not plan["reference"]:

            print("  None")

        print("\nDEFER")
        print("-----")

        for item in plan["defer"]:

            print(
                f'  ✕ {item["title"]}'
            )

            print(
                f'    Action: {item["action"]}'
            )

        if not plan["defer"]:

            print("  None")

        print("\nMode")
        print("----")

        if self.preview_mode:
            print("PREVIEW ONLY")
        else:
            print("ACTIVE")

        print(
            "\nNo applications were modified."
        )


# ==============================================
# TEST
# ==============================================

if __name__ == "__main__":

    engine = WorkspaceActionEngine()

    engine.preview()