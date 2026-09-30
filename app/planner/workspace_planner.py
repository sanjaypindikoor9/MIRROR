from app.intelligence.task_understanding import understand_workspace


class WorkspaceActionEngine:

    def __init__(self):
        self.preview_mode = True

    def create_plan(self):

        workspace = understand_workspace()

        if not workspace:
            return None

        applications = workspace["applications"]
        distractions = workspace["distractions"]
        primary_context = workspace["primary_context"]

        keep = []
        reference = []
        defer = []

        for application in applications:

            application_lower = application.lower()

            # Applications directly related to the primary task
            if primary_context == "Development":

                if any(
                    item in application_lower
                    for item in [
                        "code",
                        "pycharm",
                        "devenv",
                        "terminal",
                        "powershell",
                        "cmd"
                    ]
                ):
                    keep.append(application)

                elif application == "msedge.exe":
                    reference.append(application)

                else:
                    defer.append(application)

            elif primary_context == "Research / Browsing":

                if application == "msedge.exe":
                    keep.append(application)

                else:
                    reference.append(application)

            else:

                keep.append(application)

        # Explicit distractions always go to defer
        for distraction in distractions:

            if "instagram" in distraction.lower():
                if "msedge.exe" not in defer:
                    defer.append("msedge.exe")

        return {
            "task": workspace["current_task"],
            "primary_context": primary_context,
            "keep": list(dict.fromkeys(keep)),
            "reference": list(dict.fromkeys(reference)),
            "defer": list(dict.fromkeys(defer))
        }

    def preview(self):

        plan = self.create_plan()

        if not plan:
            print("Unable to create workspace plan.")
            return

        print("\nMIRROR WORKSPACE ACTION ENGINE")
        print("==============================")

        print(
            f'\nTask: {plan["task"]}'
        )

        print(
            f'Primary Context: '
            f'{plan["primary_context"]}'
        )

        print("\nKEEP")
        print("----")

        for application in plan["keep"]:
            print(f"  ✓ {application}")

        if not plan["keep"]:
            print("  None")

        print("\nREFERENCE")
        print("---------")

        for application in plan["reference"]:
            print(f"  → {application}")

        if not plan["reference"]:
            print("  None")

        print("\nDEFER")
        print("-----")

        for application in plan["defer"]:
            print(f"  ✕ {application}")

        if not plan["defer"]:
            print("  None")

        print("\nMode:")
        print("-----")
        print("PREVIEW ONLY")

        print(
            "\nNo applications were modified."
        )


if __name__ == "__main__":

    engine = WorkspaceActionEngine()

    engine.preview()