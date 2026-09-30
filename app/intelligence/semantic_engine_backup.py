from app.intelligence.multimodal_context import (
    build_multimodal_context
)

from app.intelligence.model_runner import (
    MirrorModelRunner
)


class SemanticEngine:

    def __init__(self, model_path=None):

        self.model_name = (
            "MIRROR Semantic Engine"
        )

        self.model_runner = (
            MirrorModelRunner(model_path)
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

        # ======================================
        # SCREEN SEMANTIC SIGNALS
        # ======================================

        programming_keywords = [

            "python",
            "code",
            "def ",
            "import ",
            "class ",
            "function",
            "terminal",
            "powershell",
            "debug",
            "error",
            "compile",
            "onnx",
            "tensorflow",
            "pytorch"
        ]

        screen_lower = (
            screen_text.lower()
        )

        programming_signals = []

        for keyword in programming_keywords:

            if keyword in screen_lower:

                programming_signals.append(
                    keyword
                )

        # ======================================
        # INTENT UNDERSTANDING
        # ======================================

        if primary_context == "Development":

            if programming_signals:

                intent = (
                    "Programming / Development"
                )

            else:

                intent = (
                    "Software Development"
                )

        elif primary_context == (
            "Research / Browsing"
        ):

            intent = (
                "Research / Information Gathering"
            )

        elif primary_context == "Reference":

            intent = (
                "Reading / Reference"
            )

        elif primary_context == "Communication":

            intent = "Communication"

        else:

            intent = (
                "General Computer Activity"
            )

        # ======================================
        # RELEVANT APPLICATIONS
        # ======================================

        relevant = []

        if active_application:

            relevant.append(
                active_application
            )

        # ======================================
        # CONFIDENCE
        # ======================================

        confidence = 0.50

        if programming_signals:

            confidence += 0.20

        if task != "General Computer Activity":

            confidence += 0.15

        if primary_context != "Unknown":

            confidence += 0.10

        confidence = min(
            confidence,
            0.95
        )

        # ======================================
        # MODEL STATUS
        # ======================================

        model_status = (
            "ONNX model loaded"
            if self.model_runner.is_loaded()
            else "Semantic reasoning mode"
        )

        # ======================================
        # RESULT
        # ======================================

        result = {

            "model": self.model_name,

            "model_status": model_status,

            "task": task,

            "intent": intent,

            "primary_context":
                primary_context,

            "active_application":
                active_application,

            "relevant_applications":
                relevant,

            "distractions":
                distractions,

            "programming_signals":
                programming_signals,

            "confidence":
                round(
                    confidence,
                    2
                )
        }

        return result


# ==============================================
# TEST
# ==============================================

if __name__ == "__main__":

    print(
        "\nMIRROR SEMANTIC ENGINE"
    )

    print(
        "======================="
    )

    context = (
        build_multimodal_context()
    )

    if context:

        engine = SemanticEngine()

        result = engine.interpret(
            context
        )

        print(
            "\nModel:"
        )

        print(
            f'  {result["model"]}'
        )

        print(
            "\nModel Status:"
        )

        print(
            f'  {result["model_status"]}'
        )

        print(
            "\nTask:"
        )

        print(
            f'  {result["task"]}'
        )

        print(
            "\nIntent:"
        )

        print(
            f'  {result["intent"]}'
        )

        print(
            "\nConfidence:"
        )

        print(
            f'  {result["confidence"]}'
        )