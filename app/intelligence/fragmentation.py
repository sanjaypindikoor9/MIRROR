from app.storage.database import initialize_database, get_recent_activity
from app.intelligence.context import classify_application


def analyze_fragmentation(limit=50):
    activities = get_recent_activity(limit)

    if not activities:
        print("No activity data available.")
        return

    contexts = []

    for activity in activities:
        context = classify_application(
            activity["process"],
            activity["title"]
        )

        contexts.append(context)

    # Count switches between different contexts
    switches = 0

    for i in range(1, len(contexts)):
        if contexts[i] != contexts[i - 1]:
            switches += 1

    # Count how many times each context appears
    context_counts = {}

    for context in contexts:
        context_counts[context] = context_counts.get(context, 0) + 1

    print("\nMIRROR CONTEXT ANALYSIS")
    print("=======================")

    print(f"\nActivities analyzed : {len(activities)}")
    print(f"Context switches    : {switches}")

    print("\nContext usage:")
    print("----------------")

    for context, count in context_counts.items():
        print(f"{context:<25} {count}")

    # Simple fragmentation score
    if len(contexts) > 1:
        fragmentation_score = (switches / (len(contexts) - 1)) * 100
    else:
        fragmentation_score = 0

    print("\nFragmentation Score:")
    print("--------------------")
    print(f"{fragmentation_score:.2f}%")

    if fragmentation_score < 20:
        status = "Focused"
    elif fragmentation_score < 50:
        status = "Moderately Fragmented"
    else:
        status = "Highly Fragmented"

    print(f"Workspace Status    : {status}")


if __name__ == "__main__":
    initialize_database()
    analyze_fragmentation()