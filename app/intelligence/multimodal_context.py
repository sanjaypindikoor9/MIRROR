from app.capture.activity import get_active_window
from app.intelligence.screen_context import analyze_screen
from app.intelligence.task_understanding import understand_workspace


def build_multimodal_context():

    # Get the currently active application
    window = get_active_window()

    if not window:
        print("No active window detected.")
        return None

    # Analyze the visible screen
    screen_result = analyze_screen(
        window["process"],
        window["title"]
    )

    # Understand the broader workspace
    workspace_result = understand_workspace()

    if not workspace_result:
        print("Unable to understand workspace.")
        return None

    result = {
        "active_application": window["process"],
        "active_window": window["title"],
        "application_context": screen_result[
            "application_context"
        ],
        "screen_text": screen_result[
            "screen_text"
        ],
        "current_task": workspace_result[
            "current_task"
        ],
        "primary_context": workspace_result[
            "primary_context"
        ],
        "workspace_state": workspace_result[
            "workspace_state"
        ],
        "fragmentation": workspace_result[
            "fragmentation"
        ],
        "distractions": workspace_result[
    "distractions"
],
"applications": workspace_result[
    "applications"
]
    }

    return result


if __name__ == "__main__":

    result = build_multimodal_context()

    if result:

        print("\nMIRROR MULTIMODAL CONTEXT")
        print("=========================")

        print(
            f'\nActive Application : '
            f'{result["active_application"]}'
        )

        print(
            f'Active Window     : '
            f'{result["active_window"]}'
        )

        print(
            f'Application Context: '
            f'{result["application_context"]}'
        )

        print(
            f'\nCurrent Task      : '
            f'{result["current_task"]}'
        )

        print(
            f'Primary Context   : '
            f'{result["primary_context"]}'
        )

        print(
            f'Workspace State   : '
            f'{result["workspace_state"]}'
        )

        print(
            f'Fragmentation     : '
            f'{result["fragmentation"]}%'
        )

        print("\nPotential Distractions:")
        print("----------------------")

        if result["distractions"]:

            for item in result["distractions"]:
                print(f"  ✕ {item}")

        else:
            print("  None detected.")

        print("\nScreen Text Sample:")
        print("-------------------")

        screen_text = result["screen_text"]

        if screen_text:

            # Only display a small portion
            print(screen_text[:1000])

        else:
            print("No screen text detected.")