from app.intelligence.multimodal_context import (
    build_multimodal_context
)

from app.intelligence.model_runner import (
    MirrorModelRunner
)


class SemanticEngine:

    def __init__(self, model_path=None):

        self.model_name = "MIRROR Semantic Engine"

        self.model_runner = MirrorModelRunner(
            model_path
        )

    def interpret(self, context):

        task = context.get(
            "current_task",
            "Unknown"
        )

        primary_context = context.get(
            "primary_context",
            "Unknown"
        )

        screen_text = context.get(
            "screen_text",
            ""
        )

        active_application = context.get(
            "active_application",
            ""
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

        applications = context.get(
            "applications",
            []
        )

        # -------------------------------------------------
        # 1. SCREEN EVIDENCE
        # -------------------------------------------------

        programming_keywords = [
            "python",
            "code",
            "def ",
            "import ",
            "class ",
            "function",
            "terminal",
            "powershell",
            "cmd",
            "debug",
            "error",
            "compile",
            "onnx",
            "tensorflow",
            "pytorch",
            "visual studio",
            "vscode"
        ]

        research_keywords = [
            "research",
            "documentation",
            "tutorial",
            "reference",
            "article",
            "github",
            "stackoverflow",
            "documentation"
        ]

        screen_lower = screen_text.lower()

        programming_signals = []
        research_signals = []

        for keyword in programming_keywords:

            if keyword in screen_lower:
                programming_signals.append(keyword)

        for keyword in research_keywords:

            if keyword in screen_lower:
                research_signals.append(keyword)

        # -------------------------------------------------
        # 2. APPLICATION EVIDENCE
        # -------------------------------------------------

        development_apps = []
        research_apps = []

        for application in applications:

            app_lower = application.lower()

            if any(
                item in app_lower
                for item in [
                    "code.exe",
                    "pycharm",
                    "devenv.exe",
                    "terminal",
                    "powershell",
                    "cmd.exe"
                ]
            ):
                development_apps.append(application)

            if any(
                item in app_lower
                for item in [
                    "msedge.exe",
                    "chrome.exe",
                    "firefox.exe"
                ]
            ):
                research_apps.append(application)

        # -------------------------------------------------
        # 3. DETERMINE INTENT
        # -------------------------------------------------

        if primary_context == "Development":

            if programming_signals:

                intent = "Programming / Development"

            else:

                intent = "Software Development"

        elif primary_context == "Research / Browsing":

            intent = "Research / Information Gathering"

        elif primary_context == "Reference":

            intent = "Reading / Reference"

        elif primary_context == "Communication":

            intent = "Communication"

        else:

            intent = "General Computer Activity"

        # -------------------------------------------------
        # 4. BUILD EVIDENCE
        # -------------------------------------------------

        evidence = []

        if development_apps:

            evidence.append(
                f"{len(development_apps)} development application(s) detected"
            )

        if research_apps:

            evidence.append(
                f"{len(research_apps)} browser application(s) detected"
            )

        if programming_signals:

            evidence.append(
                "Programming-related screen content detected"
            )

        if research_signals:

            evidence.append(
                "Research-related screen content detected"
            )

        if fragmentation >= 50:

            evidence.append(
                f"Workspace fragmentation is {fragmentation}%"
            )

        if distractions:

            evidence.append(
                f"{len(distractions)} potential distraction(s) detected"
            )

        # -------------------------------------------------
        # 5. CONFIDENCE
        # -------------------------------------------------

        confidence = 0.45

        if primary_context != "Unknown":

            confidence += 0.10

        if task != "Unknown":

            confidence += 0.10

        if programming_signals:

            confidence += 0.15

        if development_apps:

            confidence += 0.10

        if research_signals:

            confidence += 0.05

        if fragmentation >= 50:

            confidence += 0.05

        confidence = min(
            confidence,
            0.95
        )

        # -------------------------------------------------
        # 6. WORKSPACE RECOMMENDATION
        # -------------------------------------------------

        if distractions:

            recommendation = (
                "Preserve the current task and "
                "defer non-task applications."
            )

        elif fragmentation >= 50:

            recommendation = (
                "Workspace is highly fragmented. "
                "Group applications around the "
                "current task."
            )

        else:

            recommendation = (
                "Workspace is reasonably focused."
            )

        # -------------------------------------------------
        # 7. MODEL STATUS
        # -------------------------------------------------

        model_status = (
            "ONNX model loaded"
            if self.model_runner.is_loaded()
            else "Local semantic reasoning"
        )

        # -------------------------------------------------
        # 8. RETURN COMPLETE ANALYSIS
        # -------------------------------------------------

        return {

            "model": self.model_name,

            "model_status": model_status,

            "task": task,

            "intent": intent,

            "primary_context": primary_context,

            "active_application": active_application,

            "relevant_applications": (
                development_apps
                + research_apps
            ),

            "distractions": distractions,

            "programming_signals": (
                programming_signals
            ),

            "research_signals": (
                research_signals
            ),

            "evidence": evidence,

            "confidence": round(
                confidence,
                2
            ),

            "fragmentation": fragmentation,

            "workspace_state": workspace_state,

            "recommendation": recommendation
        }


if __name__ == "__main__":

    print("\nMIRROR SEMANTIC ENGINE")
    print("======================")

    context = build_multimodal_context()

    if context:

        engine = SemanticEngine()

        result = engine.interpret(
            context
        )

        print("\nModel:")
        print(
            f'  {result["model"]}'
        )

        print("\nModel Status:")
        print(
            f'  {result["model_status"]}'
        )

        print("\nTask:")
        print(
            f'  {result["task"]}'
        )

        print("\nIntent:")
        print(
            f'  {result["intent"]}'
        )

        print("\nConfidence:")
        print(
            f'  {result["confidence"]}'
        )

        print("\nEvidence:")

        for item in result["evidence"]:

            print(
                f"  ✓ {item}"
            )

        print("\nRecommendation:")

        print(
            f'  {result["recommendation"]}'
        )