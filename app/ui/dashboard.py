import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QListWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QFrame,
    QProgressBar,
)

from app.ui.styles import DARK_THEME

from app.intelligence.task_understanding import (
    understand_workspace
)

from app.intelligence.multimodal_context import (
    build_multimodal_context
)

from app.intelligence.semantic_engine import (
    SemanticEngine
)

from app.planner.workspace_actions import (
    WorkspaceActionEngine
)


class Dashboard(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "MIRROR - Workspace Intelligence"
        )

        self.resize(1100, 760)

        self.setStyleSheet(
            DARK_THEME
        )

        # ---------------------------------------------
        # ENGINES
        # ---------------------------------------------

        self.action_engine = (
            WorkspaceActionEngine()
        )

        self.semantic_engine = (
            SemanticEngine()
        )

        # ---------------------------------------------
        # MAIN WINDOW
        # ---------------------------------------------

        central = QWidget()

        self.setCentralWidget(
            central
        )

        main_layout = QVBoxLayout(
            central
        )

        main_layout.setContentsMargins(
            24,
            20,
            24,
            20
        )

        main_layout.setSpacing(
            14
        )

        # ---------------------------------------------
        # HEADER
        # ---------------------------------------------

        header_layout = QHBoxLayout()

        title_layout = QVBoxLayout()

        title = QLabel(
            "MIRROR"
        )

        title.setObjectName(
            "title"
        )

        subtitle = QLabel(
            "On-Device AI Workspace Intelligence"
        )

        subtitle.setObjectName(
            "subtitle"
        )

        title_layout.addWidget(
            title
        )

        title_layout.addWidget(
            subtitle
        )

        header_layout.addLayout(
            title_layout
        )

        header_layout.addStretch()

        self.status_label = QLabel(
            "● MIRROR ONLINE"
        )

        self.status_label.setObjectName(
            "status"
        )

        header_layout.addWidget(
            self.status_label
        )

        main_layout.addLayout(
            header_layout
        )

        # ---------------------------------------------
        # TOP INFORMATION CARDS
        # ---------------------------------------------

        cards_layout = QGridLayout()

        cards_layout.setSpacing(
            12
        )

        # Current Task

        task_card = self.create_card()

        task_layout = QVBoxLayout(
            task_card
        )

        task_label = QLabel(
            "CURRENT TASK"
        )

        task_label.setObjectName(
            "cardTitle"
        )

        self.task_value = QLabel(
            "Analyzing..."
        )

        self.task_value.setObjectName(
            "task"
        )

        task_layout.addWidget(
            task_label
        )

        task_layout.addWidget(
            self.task_value
        )

        cards_layout.addWidget(
            task_card,
            0,
            0
        )

        # Primary Context

        context_card = self.create_card()

        context_layout = QVBoxLayout(
            context_card
        )

        context_label = QLabel(
            "PRIMARY CONTEXT"
        )

        context_label.setObjectName(
            "cardTitle"
        )

        self.context_value = QLabel(
            "Analyzing..."
        )

        self.context_value.setObjectName(
            "task"
        )

        context_layout.addWidget(
            context_label
        )

        context_layout.addWidget(
            self.context_value
        )

        cards_layout.addWidget(
            context_card,
            0,
            1
        )

        # Workspace State

        state_card = self.create_card()

        state_layout = QVBoxLayout(
            state_card
        )

        state_label = QLabel(
            "WORKSPACE STATE"
        )

        state_label.setObjectName(
            "cardTitle"
        )

        self.state_value = QLabel(
            "Analyzing..."
        )

        self.state_value.setObjectName(
            "task"
        )

        state_layout.addWidget(
            state_label
        )

        state_layout.addWidget(
            self.state_value
        )

        cards_layout.addWidget(
            state_card,
            0,
            2
        )

        main_layout.addLayout(
            cards_layout
        )

        # ---------------------------------------------
        # MIDDLE SECTION
        # ---------------------------------------------

        middle_layout = QHBoxLayout()

        middle_layout.setSpacing(
            12
        )

        # ---------------------------------------------
        # WORKSPACE
        # ---------------------------------------------

        workspace_card = self.create_card()

        workspace_layout = QVBoxLayout(
            workspace_card
        )

        workspace_title = QLabel(
            "WORKSPACE"
        )

        workspace_title.setObjectName(
            "cardTitle"
        )

        workspace_layout.addWidget(
            workspace_title
        )

        self.workspace_list = QListWidget()

        self.workspace_list.setMaximumHeight(
            100
        )

        workspace_layout.addWidget(
            self.workspace_list
        )

        middle_layout.addWidget(
            workspace_card,
            1
        )

        # ---------------------------------------------
        # RECENT ACTIVITY
        # ---------------------------------------------

        activity_card = self.create_card()

        activity_layout = QVBoxLayout(
            activity_card
        )

        activity_title = QLabel(
            "RECENT ACTIVITY"
        )

        activity_title.setObjectName(
            "cardTitle"
        )

        activity_layout.addWidget(
            activity_title
        )

        self.activity_list = QListWidget()

        self.activity_list.setMaximumHeight(
            100
        )

        activity_layout.addWidget(
            self.activity_list
        )

        middle_layout.addWidget(
            activity_card,
            1
        )

        main_layout.addLayout(
            middle_layout
        )

        # ---------------------------------------------
        # AI INSIGHT CARD
        # ---------------------------------------------

        ai_card = self.create_card()

        ai_layout = QVBoxLayout(
            ai_card
        )

        ai_title = QLabel(
            "AI INSIGHT"
        )

        ai_title.setObjectName(
            "cardTitle"
        )

        ai_layout.addWidget(
            ai_title
        )

        # Intent

        intent_row = QHBoxLayout()

        intent_label = QLabel(
            "Intent:"
        )

        self.intent_value = QLabel(
            "Analyzing..."
        )

        intent_row.addWidget(
            intent_label
        )

        intent_row.addWidget(
            self.intent_value
        )

        intent_row.addStretch()

        ai_layout.addLayout(
            intent_row
        )

        # Confidence

        confidence_row = QHBoxLayout()

        confidence_label = QLabel(
            "Confidence:"
        )

        self.confidence_value = QLabel(
            "0%"
        )

        confidence_row.addWidget(
            confidence_label
        )

        confidence_row.addWidget(
            self.confidence_value
        )

        confidence_row.addStretch()

        ai_layout.addLayout(
            confidence_row
        )

        # Evidence

        evidence_label = QLabel(
            "Evidence:"
        )

        ai_layout.addWidget(
            evidence_label
        )

        self.evidence_list = QListWidget()

        self.evidence_list.setMaximumHeight(
            80
        )

        ai_layout.addWidget(
            self.evidence_list
        )

        # Recommendation

        recommendation_label = QLabel(
            "Recommendation:"
        )

        ai_layout.addWidget(
            recommendation_label
        )

        self.recommendation_value = QLabel(
            "Analyzing workspace..."
        )

        self.recommendation_value.setWordWrap(
            True
        )

        ai_layout.addWidget(
            self.recommendation_value
        )

        main_layout.addWidget(
            ai_card
        )

        # ---------------------------------------------
        # FRAGMENTATION
        # ---------------------------------------------

        fragmentation_card = self.create_card()

        fragmentation_layout = QVBoxLayout(
            fragmentation_card
        )

        fragmentation_header = QHBoxLayout()

        fragmentation_title = QLabel(
            "CONTEXT FRAGMENTATION"
        )

        fragmentation_title.setObjectName(
            "cardTitle"
        )

        self.fragmentation_value = QLabel(
            "0%"
        )

        fragmentation_header.addWidget(
            fragmentation_title
        )

        fragmentation_header.addStretch()

        fragmentation_header.addWidget(
            self.fragmentation_value
        )

        fragmentation_layout.addLayout(
            fragmentation_header
        )

        self.fragmentation_bar = QProgressBar()

        self.fragmentation_bar.setRange(
            0,
            100
        )

        self.fragmentation_bar.setValue(
            0
        )

        self.fragmentation_bar.setTextVisible(
            False
        )

        fragmentation_layout.addWidget(
            self.fragmentation_bar
        )

        self.fragmentation_status = QLabel(
            "Analyzing..."
        )

        fragmentation_layout.addWidget(
            self.fragmentation_status
        )

        main_layout.addWidget(
            fragmentation_card
        )

        # ---------------------------------------------
        # WORKSPACE PLAN
        # ---------------------------------------------

        plan_card = self.create_card()

        plan_layout = QVBoxLayout(
            plan_card
        )

        plan_title = QLabel(
            "WORKSPACE PLAN"
        )

        plan_title.setObjectName(
            "cardTitle"
        )

        plan_layout.addWidget(
            plan_title
        )

        self.plan_list = QListWidget()

        self.plan_list.setMaximumHeight(
            90
        )

        plan_layout.addWidget(
            self.plan_list
        )

        main_layout.addWidget(
            plan_card
        )

        # ---------------------------------------------
        # BUTTONS
        # ---------------------------------------------

        button_layout = QHBoxLayout()

        button_layout.addStretch()

        self.refresh_button = QPushButton(
            "Refresh Analysis"
        )

        self.refresh_button.clicked.connect(
            self.refresh_dashboard
        )

        button_layout.addWidget(
            self.refresh_button
        )

        self.preview_button = QPushButton(
            "Preview Workspace"
        )

        self.preview_button.clicked.connect(
            self.preview_workspace
        )

        button_layout.addWidget(
            self.preview_button
        )

        self.apply_button = QPushButton(
            "Apply Workspace"
        )

        self.apply_button.clicked.connect(
            self.apply_workspace
        )

        button_layout.addWidget(
            self.apply_button
        )

        main_layout.addLayout(
            button_layout
        )

        # ---------------------------------------------
        # INITIAL ANALYSIS
        # ---------------------------------------------

        self.refresh_dashboard()

    # =================================================
    # CARD CREATOR
    # =================================================

    def create_card(self):

        card = QFrame()

        card.setObjectName(
            "card"
        )

        return card

    # =================================================
    # REFRESH DASHBOARD
    # =================================================

    def refresh_dashboard(self):

        try:

            workspace = understand_workspace(
                50
            )

            if not workspace:

                return

            # -----------------------------------------
            # BASIC WORKSPACE DATA
            # -----------------------------------------

            task = workspace.get(
                "current_task",
                "Unknown"
            )

            primary_context = workspace.get(
                "primary_context",
                "Unknown"
            )

            workspace_state = workspace.get(
                "workspace_state",
                "Unknown"
            )

            fragmentation = workspace.get(
                "fragmentation",
                0
            )

            applications = workspace.get(
                "applications",
                []
            )

            distractions = workspace.get(
                "distractions",
                []
            )

            # -----------------------------------------
            # TOP CARDS
            # -----------------------------------------

            self.task_value.setText(
                task
            )

            self.context_value.setText(
                primary_context
            )

            self.state_value.setText(
                workspace_state
            )

            # -----------------------------------------
            # FRAGMENTATION
            # -----------------------------------------

            self.fragmentation_value.setText(
                f"{fragmentation:.0f}%"
            )

            self.fragmentation_bar.setValue(
                int(fragmentation)
            )

            if fragmentation < 20:

                fragmentation_text = (
                    "Focused"
                )

            elif fragmentation < 50:

                fragmentation_text = (
                    "Moderately Fragmented"
                )

            else:

                fragmentation_text = (
                    "Highly Fragmented"
                )

            self.fragmentation_status.setText(
                fragmentation_text
            )

            # -----------------------------------------
            # WORKSPACE LIST
            # -----------------------------------------

            self.workspace_list.clear()

            seen_apps = set()

            for application in applications:

                if application in seen_apps:
                    continue

                seen_apps.add(
                    application
                )

                self.workspace_list.addItem(
                    f"✓ {application}"
                )

            # -----------------------------------------
            # RECENT ACTIVITY
            # -----------------------------------------

            from app.storage.database import (
                get_recent_activity
            )

            activities = get_recent_activity(
                20
            )

            self.activity_list.clear()

            seen_activity = set()

            for activity in activities:

                process = activity[
                    "process"
                ]

                title = activity[
                    "title"
                ]

                key = (
                    process,
                    title
                )

                if key in seen_activity:

                    continue

                seen_activity.add(
                    key
                )

                display_title = (
                    title
                    if title
                    else process
                )

                self.activity_list.addItem(
                    f"• {display_title}"
                )

            # -----------------------------------------
            # AI SEMANTIC ANALYSIS
            # -----------------------------------------

            context = (
                build_multimodal_context()
            )

            if context:

                # Ensure application information
                # is available to the semantic engine.

                context[
                    "applications"
                ] = applications

                semantic_result = (
                    self.semantic_engine.interpret(
                        context
                    )
                )

                # Intent

                self.intent_value.setText(
                    semantic_result.get(
                        "intent",
                        "Unknown"
                    )
                )

                # Confidence

                confidence = semantic_result.get(
                    "confidence",
                    0
                )

                self.confidence_value.setText(
                    f"{int(confidence * 100)}%"
                )

                # Evidence

                self.evidence_list.clear()

                evidence = semantic_result.get(
                    "evidence",
                    []
                )

                for item in evidence:

                    self.evidence_list.addItem(
                        f"✓ {item}"
                    )

                if not evidence:

                    self.evidence_list.addItem(
                        "No additional evidence detected."
                    )

                # Recommendation

                self.recommendation_value.setText(
                    semantic_result.get(
                        "recommendation",
                        "No recommendation available."
                    )
                )

            # -----------------------------------------
            # WORKSPACE PLAN
            # -----------------------------------------

            self.update_workspace_plan()

        except Exception as error:

            print(
                "Dashboard refresh error:",
                error
            )

    # =================================================
    # WORKSPACE PLAN
    # =================================================

    def update_workspace_plan(self):

        try:

            plan = (
                self.action_engine.create_plan()
            )

            if not plan:

                return

            self.plan_list.clear()

            # -----------------------------------------
            # KEEP
            # -----------------------------------------

            for item in plan["keep"][:3]:

                self.plan_list.addItem(
                    f'✓ KEEP  {item["title"]}'
                )

            # -----------------------------------------
            # REFERENCE
            # -----------------------------------------

            for item in plan["reference"][:3]:

                self.plan_list.addItem(
                    f'→ REFERENCE  {item["title"]}'
                )

            # -----------------------------------------
            # DEFER
            # -----------------------------------------

            for item in plan["defer"][:3]:

                self.plan_list.addItem(
                    f'✕ DEFER  {item["title"]}'
                )

            if self.plan_list.count() == 0:

                self.plan_list.addItem(
                    "Workspace is already organized."
                )

        except Exception as error:

            print(
                "Workspace plan error:",
                error
            )

    # =================================================
    # PREVIEW WORKSPACE
    # =================================================

    def preview_workspace(self):

        self.action_engine.preview_mode = True

        self.action_engine.window_controller.preview_mode = True

        self.action_engine.preview()

    # =================================================
    # APPLY WORKSPACE
    # =================================================

    def apply_workspace(self):

        plan = (
            self.action_engine.create_plan()
        )

        if not plan:

            return

        # Temporarily enable real actions.

        self.action_engine.preview_mode = False

        self.action_engine.window_controller.preview_mode = False

        self.action_engine.apply_plan(
            plan
        )

        # Restore preview mode after execution.

        self.action_engine.preview_mode = True

        self.action_engine.window_controller.preview_mode = True

        # Refresh dashboard.

        self.refresh_dashboard()

    # =================================================
    # CLOSE
    # =================================================

    def closeEvent(self, event):

        event.accept()


# =====================================================
# MAIN
# =====================================================

def main():

    app = QApplication(
        sys.argv
    )

    app.setStyleSheet(
        DARK_THEME
    )

    window = Dashboard()

    window.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":

    main()