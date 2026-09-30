from app.storage.database import get_recent_activity
from app.intelligence.context import classify_application


def detect_task(limit=50):
    activities = get_recent_activity(limit)

    if not activities:
        print("No activity data available.")
        return None

    contexts = {}

    for activity in activities:
        context = classify_application(
            activity["process"],
            activity["title"]
        )

        if context not in contexts:
            contexts[context] = []

        contexts[context].append({
            "process": activity["process"],
            "title": activity["title"]
        })

    print("\nMIRROR TASK DETECTOR")
    print("====================")

    print("\nDetected workspace contexts:")
    print("----------------------------")

    for context, items in contexts.items():
        print(f"\n[{context}]")

        for item in items:
            print(f'  └── {item["title"] or item["process"]}')

    # Simple task inference based on dominant context
    dominant_context = max(
        contexts,
        key=lambda context: len(contexts[context])
    )

    task_map = {
        "Development": "Software Development",
        "Research / Browsing": "Research / Study",
        "Reference": "Reading / Reference",
        "AI Assistant": "AI-Assisted Work",
        "Communication": "Communication",
        "File Management": "File Management"
    }

    detected_task = task_map.get(
        dominant_context,
        "General Computer Activity"
    )

    print("\nDetected Current Task:")
    print("----------------------")
    print(detected_task)

    print(f"\nPrimary Context: {dominant_context}")

    return {
        "task": detected_task,
        "primary_context": dominant_context,
        "contexts": contexts
    }


if __name__ == "__main__":
    detect_task()