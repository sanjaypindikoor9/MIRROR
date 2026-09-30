import json


class MirrorAIEngine:
    """
    Central AI interface for MIRROR.

    The current version provides structured workspace
    reasoning without requiring a cloud API.

    A Snapdragon/Qualcomm AI Hub model can later be
    connected through this same interface.
    """

    def __init__(self):
        self.model_name = "MIRROR-Local-Reasoning"

    def analyze(self, context):

        task = context.get(
            "current_task",
            "Unknown"
        )

        primary_context = context.get(
            "primary_context",
            "Unknown"
        )

        applications = context.get(
            "applications",
            []
        )

        distractions = context.get(
            "distractions",
            []
        )

        fragmentation = context.get(
            "fragmentation",
            0
        )

        workspace_state = context.get(
            "workspace_state",
            "Unknown"
        )

        # Determine relevant applications
        relevant = []

        for application in applications:

            application_lower = application.lower()

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
                    relevant.append(application)

            elif primary_context == "Research / Browsing":

                if any(
                    item in application_lower
                    for item in [
                        "edge",
                        "chrome",
                        "firefox"
                    ]
                ):
                    relevant.append(application)

            else:

                relevant.append(application)

        # Generate workspace recommendation
        if distractions:

            recommendation = (
                "Preserve the current task and defer "
                "non-task applications."
            )

        elif fragmentation >= 50:

            recommendation = (
                "Workspace is highly fragmented. "
                "Group applications around the current task."
            )

        else:

            recommendation = (
                "Workspace is reasonably focused."
            )

        result = {
            "model": self.model_name,
            "task": task,
            "primary_context": primary_context,
            "relevant_applications": relevant,
            "distractions": distractions,
            "fragmentation": fragmentation,
            "workspace_state": workspace_state,
            "recommendation": recommendation
        }

        return result


def print_analysis(result):

    print("\nMIRROR AI ANALYSIS")
    print("==================")

    print(
        f'\nModel              : '
        f'{result["model"]}'
    )

    print(
        f'Task               : '
        f'{result["task"]}'
    )

    print(
        f'Primary Context    : '
        f'{result["primary_context"]}'
    )

    print(
        f'Workspace State    : '
        f'{result["workspace_state"]}'
    )

    print(
        f'Fragmentation      : '
        f'{result["fragmentation"]}%'
    )

    print("\nRelevant Applications:")
    print("----------------------")

    if result["relevant_applications"]:

        for application in result["relevant_applications"]:
            print(f"  ✓ {application}")

    else:

        print("  None identified.")

    print("\nDistractions:")
    print("------------")

    if result["distractions"]:

        for distraction in result["distractions"]:
            print(f"  ✕ {distraction}")

    else:

        print("  None detected.")

    print("\nRecommendation:")
    print("---------------")
    print(result["recommendation"])


if __name__ == "__main__":

    from app.intelligence.task_understanding import (
        understand_workspace
    )

    workspace = understand_workspace()

    if workspace:

        engine = MirrorAIEngine()

        analysis = engine.analyze(
            workspace
        )

        print_analysis(analysis)