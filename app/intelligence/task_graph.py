from collections import defaultdict


class TaskGraph:
    def __init__(self):
        self.contexts = defaultdict(list)

    def add_application(self, application, context):
        if application not in self.contexts[context]:
            self.contexts[context].append(application)

    def build_from_activity(self, activities):
        """
        Build a workspace graph from activity records.

        Each activity should contain:
        process, title, and context.
        """

        self.contexts.clear()

        for activity in activities:
            self.add_application(
                activity["process"],
                activity["context"]
            )

    def get_workspace(self):
        return dict(self.contexts)

    def display_workspace(self):
        print("\nMIRROR WORKSPACE")
        print("================")

        if not self.contexts:
            print("No workspace data available.")
            return

        for context, applications in self.contexts.items():
            print(f"\n[{context}]")

            for application in applications:
                print(f"  └── {application}")


if __name__ == "__main__":

    # Sample workspace data
    activities = [
        {
            "process": "Code.exe",
            "title": "activity.py",
            "context": "Development"
        },
        {
            "process": "msedge.exe",
            "title": "Google",
            "context": "Research / Browsing"
        },
        {
            "process": "ChatGPT Classic.exe",
            "title": "Greeting Nova",
            "context": "AI Assistant"
        },
        {
            "process": "explorer.exe",
            "title": "",
            "context": "File Management"
        }
    ]

    graph = TaskGraph()

    graph.build_from_activity(activities)

    graph.display_workspace()