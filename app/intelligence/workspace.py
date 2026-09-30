from app.storage.database import initialize_database, get_recent_activity
from app.intelligence.context import classify_application
from app.intelligence.task_graph import TaskGraph


def build_workspace():
    activities = get_recent_activity(50)

    workspace_activities = []

    for activity in activities:
        context = classify_application(
            activity["process"],
            activity["title"]
        )

        workspace_activities.append({
            "process": activity["process"],
            "title": activity["title"],
            "context": context
        })

    graph = TaskGraph()
    graph.build_from_activity(workspace_activities)

    return graph


if __name__ == "__main__":
    initialize_database()

    graph = build_workspace()

    graph.display_workspace()