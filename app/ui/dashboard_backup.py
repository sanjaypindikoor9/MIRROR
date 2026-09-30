import sys
from datetime import datetime

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QListWidget,
    QListWidgetItem,
    QProgressBar,
    QPushButton,
)

from PySide6.QtCore import QTimer

from app.ui.styles import DARK_THEME

from app.intelligence.task_detector import detect_task
from app.storage.database import get_recent_activity
from app.intelligence.context import classify_application

from app.planner.workspace_actions import (
    WorkspaceActionEngine
)


class MirrorDashboard(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "MIRROR — Workspace Intelligence"
        )

        self.resize(1100, 700)

        self.action_engine = (
            WorkspaceActionEngine()
        )

        # Safety: start in preview mode
        self.action_engine.preview_mode = True
        self.action_engine.window_controller.preview_mode = True

        self.build_ui()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.load_data)
        self.timer.start(2000)

        self.load_data()

    # ==========================================
    # CARD CREATION
    # ==========================================

    def create_card(self):

        card = QFrame()
        card.setObjectName("card")

        layout = QVBoxLayout(card)

        layout.setContentsMargins(
            20,
            15,
            20,
            15
        )

        return card, layout

    # ==========================================
    # BUILD UI
    # ==========================================

    def build_ui(self):

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)

        main_layout.setContentsMargins(
            30,
            20,
            30,
            20
        )

        main_layout.setSpacing(12)

        # ======================================
        # HEADER
        # ======================================

        header_layout = QHBoxLayout()

        header_left = QVBoxLayout()

        title = QLabel("MIRROR")
        title.setObjectName("title")

        subtitle = QLabel(
            "On-Device AI Workspace Intelligence Engine"
        )

        subtitle.setObjectName("subtitle")

        header_left.addWidget(title)
        header_left.addWidget(subtitle)

        header_layout.addLayout(header_left)
        header_layout.addStretch()

        status = QLabel(
            "●  MIRROR ONLINE"
        )

        status.setObjectName("status")

        header_layout.addWidget(status)

        main_layout.addLayout(header_layout)

        # ======================================
        # TOP CARDS
        # ======================================

        top_layout = QHBoxLayout()
        top_layout.setSpacing(12)

        # CURRENT TASK

        task_card, task_layout = self.create_card()

        task_label = QLabel("CURRENT TASK")
        task_label.setObjectName("cardTitle")

        self.task_value = QLabel("Detecting...")
        self.task_value.setObjectName("task")

        task_layout.addWidget(task_label)
        task_layout.addWidget(self.task_value)

        top_layout.addWidget(task_card)

        # PRIMARY CONTEXT

        context_card, context_layout = self.create_card()

        context_label = QLabel("PRIMARY CONTEXT")
        context_label.setObjectName("cardTitle")

        self.context_value = QLabel("Detecting...")
        self.context_value.setObjectName("task")

        context_layout.addWidget(context_label)
        context_layout.addWidget(self.context_value)

        top_layout.addWidget(context_card)

        main_layout.addLayout(top_layout)

        # ======================================
        # WORKSPACE
        # ======================================

        workspace_card, workspace_layout = self.create_card()

        workspace_title = QLabel("WORKSPACE")
        workspace_title.setObjectName("cardTitle")

        self.workspace_list = QListWidget()

        # Prevent the list from consuming the whole window
        self.workspace_list.setMaximumHeight(70)

        workspace_layout.addWidget(workspace_title)
        workspace_layout.addWidget(self.workspace_list)

        main_layout.addWidget(workspace_card)

        # ======================================
        # RECENT ACTIVITY
        # ======================================

        activity_card, activity_layout = self.create_card()

        activity_title = QLabel("RECENT ACTIVITY")
        activity_title.setObjectName("cardTitle")

        self.activity_list = QListWidget()

        # Prevent the activity list from consuming the whole window
        self.activity_list.setMaximumHeight(90)

        activity_layout.addWidget(activity_title)
        activity_layout.addWidget(self.activity_list)

        main_layout.addWidget(activity_card)

        # ======================================
        # BOTTOM CARDS
        # ======================================

        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(12)

        # CONTEXT FRAGMENTATION

        fragmentation_card, fragmentation_layout = (
            self.create_card()
        )

        fragmentation_title = QLabel(
            "CONTEXT FRAGMENTATION"
        )

        fragmentation_title.setObjectName(
            "cardTitle"
        )

        self.fragmentation_bar = QProgressBar()

        self.fragmentation_bar.setRange(
            0,
            100
        )

        self.fragmentation_bar.setValue(0)

        self.fragmentation_bar.setTextVisible(
            False
        )

        self.fragmentation_status = QLabel(
            "Analyzing..."
        )

        self.fragmentation_status.setObjectName(
            "status"
        )

        fragmentation_layout.addWidget(
            fragmentation_title
        )

        fragmentation_layout.addWidget(
            self.fragmentation_bar
        )

        fragmentation_layout.addWidget(
            self.fragmentation_status
        )

        bottom_layout.addWidget(
            fragmentation_card
        )

        # RECOMMENDATION

        recommendation_card, recommendation_layout = (
            self.create_card()
        )

        recommendation_title = QLabel(
            "RECOMMENDATION"
        )

        recommendation_title.setObjectName(
            "cardTitle"
        )

        self.recommendation = QLabel(
            "Analyzing workspace..."
        )

        self.recommendation.setWordWrap(
            True
        )

        recommendation_layout.addWidget(
            recommendation_title
        )

        recommendation_layout.addWidget(
            self.recommendation
        )

        bottom_layout.addWidget(
            recommendation_card
        )

        main_layout.addLayout(bottom_layout)

        # ======================================
        # WORKSPACE PLAN
        # ======================================

        action_card, action_layout = self.create_card()

        action_title = QLabel(
            "WORKSPACE PLAN"
        )

        action_title.setObjectName(
            "cardTitle"
        )

        self.workspace_plan = QLabel(
            "Generating workspace plan..."
        )

        self.workspace_plan.setWordWrap(True)

        action_layout.addWidget(action_title)
        action_layout.addWidget(self.workspace_plan)

        main_layout.addWidget(action_card)

        # ======================================
        # BUTTONS
        # ======================================

        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)

        self.preview_button = QPushButton(
            "PREVIEW WORKSPACE"
        )

        self.preview_button.clicked.connect(
            self.preview_workspace_action
        )

        button_layout.addWidget(
            self.preview_button
        )

        self.apply_button = QPushButton(
            "APPLY WORKSPACE"
        )

        self.apply_button.clicked.connect(
            self.apply_workspace_action
        )

        button_layout.addWidget(
            self.apply_button
        )

        main_layout.addLayout(button_layout)

        # ======================================
        # MODE
        # ======================================

        self.mode_label = QLabel(
            "MODE: PREVIEW ONLY"
        )

        self.mode_label.setObjectName(
            "status"
        )

        main_layout.addWidget(
            self.mode_label
        )

    # ==========================================
    # LOAD DATA
    # ==========================================

    def load_data(self):

        try:

            result = detect_task()

            if not result:

                self.task_value.setText(
                    "No activity"
                )

                self.context_value.setText(
                    "Unknown"
                )

                return

            # ==================================
            # TASK
            # ==================================

            self.task_value.setText(
                result["task"]
            )

            self.context_value.setText(
                result["primary_context"]
            )

            # ==================================
            # WORKSPACE
            # ==================================

            self.workspace_list.clear()

            contexts = result["contexts"]

            for context, activities in contexts.items():

                item = QListWidgetItem(
                    f"{context}   •   "
                    f"{len(activities)} activities"
                )

                self.workspace_list.addItem(item)

            # ==================================
            # RECENT ACTIVITY
            # ==================================

            self.update_activity_timeline()

            # ==================================
            # FRAGMENTATION
            # ==================================

            activities = get_recent_activity(50)

            context_sequence = []

            for activity in activities:

                context = classify_application(
                    activity["process"],
                    activity["title"]
                )

                context_sequence.append(context)

            switches = 0

            for i in range(
                1,
                len(context_sequence)
            ):

                if (
                    context_sequence[i]
                    != context_sequence[i - 1]
                ):

                    switches += 1

            if len(context_sequence) > 1:

                score = (
                    switches
                    / (len(context_sequence) - 1)
                ) * 100

            else:

                score = 0

            score = int(score)

            self.fragmentation_bar.setValue(
                score
            )

            if score < 20:

                status = "Focused"

            elif score < 50:

                status = "Moderately Fragmented"

            else:

                status = "Highly Fragmented"

            self.fragmentation_status.setText(
                f"{score}% — {status}"
            )

            # ==================================
            # RECOMMENDATION
            # ==================================

            recommendation = (
                self.generate_recommendation(
                    contexts
                )
            )

            self.recommendation.setText(
                recommendation
            )

            # ==================================
            # WORKSPACE PLAN
            # ==================================

            self.update_workspace_plan()

        except Exception as error:

            self.recommendation.setText(
                f"Monitoring error: {error}"
            )

    # ==========================================
    # ACTIVITY TIMELINE
    # ==========================================

    def update_activity_timeline(self):

        activities = get_recent_activity(8)

        self.activity_list.clear()

        if not activities:

            self.activity_list.addItem(
                "No recent activity."
            )

            return

        shown_titles = set()

        for activity in activities:

            timestamp = activity["timestamp"]

            process = activity["process"]

            title = (
                activity["title"]
                or process
            )

            # Avoid repeated identical entries
            if title in shown_titles:
                continue

            shown_titles.add(title)

            context = classify_application(
                process,
                title
            )

            try:

                time_value = datetime.fromisoformat(
                    timestamp
                ).strftime("%H:%M:%S")

            except ValueError:

                time_value = timestamp

            distraction_words = [
                "instagram",
                "facebook",
                "netflix",
                "youtube",
                "reddit",
                "twitter",
                "x.com"
            ]

            is_distraction = any(
                word in title.lower()
                for word in distraction_words
            )

            if is_distraction:

                display_text = (
                    f"{time_value}   ⚠   "
                    f"{title}   •   "
                    f"Distraction"
                )

            else:

                display_text = (
                    f"{time_value}   •   "
                    f"{title}   •   "
                    f"{context}"
                )

            self.activity_list.addItem(
                display_text
            )

    # ==========================================
    # RECOMMENDATION ENGINE
    # ==========================================

    def generate_recommendation(
        self,
        contexts
    ):

        recommendations = []

        distraction_words = [
            "instagram",
            "facebook",
            "netflix",
            "youtube",
            "reddit",
            "twitter",
            "x.com"
        ]

        seen = set()

        for context, activities in contexts.items():

            for activity in activities:

                title = (
                    activity["title"]
                    or activity["process"]
                )

                title_lower = title.lower()

                if any(
                    word in title_lower
                    for word in distraction_words
                ):

                    if title not in seen:

                        recommendations.append(
                            f"Defer {title}"
                        )

                        seen.add(title)

        if recommendations:

            return " • ".join(
                recommendations[:3]
            )

        return (
            "Workspace looks organized "
            "for the current task."
        )

    # ==========================================
    # UPDATE WORKSPACE PLAN
    # ==========================================

    def update_workspace_plan(self):

        plan = (
            self.action_engine.create_plan()
        )

        if not plan:

            self.workspace_plan.setText(
                "Unable to generate "
                "workspace plan."
            )

            return

        lines = []

        lines.append(
            f'Task: {plan["task"]}'
        )

        lines.append("")

        lines.append("✓ KEEP")

        for item in plan["keep"][:3]:

            lines.append(
                f'   {item["title"]}'
            )

        if not plan["keep"]:

            lines.append("   None")

        lines.append("")

        lines.append("→ REFERENCE")

        for item in plan["reference"][:3]:

            lines.append(
                f'   {item["title"]}'
            )

        if not plan["reference"]:

            lines.append("   None")

        lines.append("")

        lines.append("✕ DEFER")

        for item in plan["defer"][:3]:

            lines.append(
                f'   {item["title"]}'
            )

        if not plan["defer"]:

            lines.append("   None")

        lines.append("")

        lines.append(
            "Mode: PREVIEW ONLY"
        )

        self.workspace_plan.setText(
            "\n".join(lines)
        )

    # ==========================================
    # PREVIEW WORKSPACE
    # ==========================================

    def preview_workspace_action(self):

        plan = (
            self.action_engine.create_plan()
        )

        if not plan:

            self.workspace_plan.setText(
                "Unable to create "
                "workspace plan."
            )

            return

        lines = [
            "MIRROR WORKSPACE PREVIEW",
            "",
            f'Task: {plan["task"]}',
            "",
            "MIRROR would:",
            ""
        ]

        for item in plan["keep"][:5]:

            lines.append(
                f'✓ Restore: {item["title"]}'
            )

        for item in plan["reference"][:5]:

            lines.append(
                f'→ Restore: {item["title"]}'
            )

        for item in plan["defer"][:5]:

            lines.append(
                f'✕ Minimize: {item["title"]}'
            )

        lines.append("")

        lines.append(
            "PREVIEW ONLY — no changes made."
        )

        self.workspace_plan.setText(
            "\n".join(lines)
        )

    # ==========================================
    # APPLY WORKSPACE
    # ==========================================

    def apply_workspace_action(self):

        plan = (
            self.action_engine.create_plan()
        )

        if not plan:

            self.workspace_plan.setText(
                "Unable to create "
                "workspace plan."
            )

            return

        self.action_engine.preview_mode = False

        self.action_engine.window_controller.preview_mode = False

        self.mode_label.setText(
            "MODE: ACTIVE — APPLYING WORKSPACE"
        )

        QApplication.processEvents()

        self.action_engine.apply_plan(plan)

        self.action_engine.preview_mode = True

        self.action_engine.window_controller.preview_mode = True

        self.mode_label.setText(
            "MODE: PREVIEW ONLY"
        )

        self.workspace_plan.setText(
            "✓ Workspace actions applied.\n\n"
            "MIRROR restored relevant windows "
            "and minimized deferred windows."
        )


# ==============================================
# APPLICATION ENTRY POINT
# ==============================================

def main():

    app = QApplication(sys.argv)

    app.setStyleSheet(
        DARK_THEME
    )

    window = MirrorDashboard()

    window.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":

    main()