from app.storage.database import get_recent_activity
from app.intelligence.context import classify_application


def understand_workspace(limit=50):

    activities = get_recent_activity(limit)

    if not activities:
        print("No activity data available.")
        return None

    context_counts = {}
    applications = []
    distractions = []

    distraction_words = [
        "instagram",
        "facebook",
        "netflix",
        "youtube",
        "reddit",
        "twitter",
        "x.com"
    ]

    for activity in activities:

        process = activity["process"]
        title = activity["title"] or process

        context = classify_application(
            process,
            title
        )

        context_counts[context] = (
            context_counts.get(context, 0) + 1
        )

        if process not in applications:
            applications.append(process)

        title_lower = title.lower()

        if any(
            word in title_lower
            for word in distraction_words
        ):
            if title not in distractions:
                distractions.append(title)

    # Find the dominant workspace context
    primary_context = max(
        context_counts,
        key=context_counts.get
    )

    task_map = {
        "Development": "Software Development",
        "Research / Browsing": "Research / Study",
        "Reference": "Reading / Reference",
        "AI Assistant": "AI-Assisted Work",
        "Communication": "Communication",
        "File Management": "File Management"
    }

    current_task = task_map.get(
        primary_context,
        "General Computer Activity"
    )

    # Determine workspace state
    total_switches = 0

    previous_context = None

    for activity in activities:

        context = classify_application(
            activity["process"],
            activity["title"]
        )

        if (
            previous_context is not None
            and context != previous_context
        ):
            total_switches += 1

        previous_context = context

    if len(activities) > 1:

        fragmentation = (
            total_switches /
            (len(activities) - 1)
        ) * 100

    else:

        fragmentation = 0

    if fragmentation < 20:
        workspace_state = "Focused"

    elif fragmentation < 50:
        workspace_state = "Moderately Fragmented"

    else:
        workspace_state = "Highly Fragmented"

    result = {
        "current_task": current_task,
        "primary_context": primary_context,
        "applications": applications,
        "distractions": distractions,
        "fragmentation": round(fragmentation, 2),
        "workspace_state": workspace_state
    }

    return result


if __name__ == "__main__":

    result = understand_workspace()

    if result:

        print("\nMIRROR TASK UNDERSTANDING")
        print("=========================")

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

        print("\nApplications:")
        print("------------")

        for application in result["applications"]:
            print(f"  ✓ {application}")

        print("\nPotential Distractions:")
        print("----------------------")

        if result["distractions"]:

            for distraction in result["distractions"]:
                print(f"  ✕ {distraction}")

        else:
            print("  None detected.")