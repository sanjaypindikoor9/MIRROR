DARK_THEME = """
QMainWindow {
    background-color: #0b0f14;
}

QWidget {
    color: #e6edf3;
    font-family: "Segoe UI";
}

QLabel#title {
    font-size: 30px;
    font-weight: bold;
}

QLabel#subtitle {
    color: #8b949e;
    font-size: 13px;
}

QFrame#card {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
}

QLabel#cardTitle {
    color: #8b949e;
    font-size: 12px;
    font-weight: bold;
}

QLabel#task {
    font-size: 22px;
    font-weight: bold;
}

QLabel#status {
    font-size: 15px;
    font-weight: bold;
}

QProgressBar {
    background-color: #21262d;
    border: none;
    border-radius: 6px;
    height: 10px;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #58a6ff;
    border-radius: 6px;
}

QListWidget {
    background-color: transparent;
    border: none;
    outline: none;
}

QListWidget::item {
    padding: 8px;
    border-radius: 6px;
}

QListWidget::item:hover {
    background-color: #21262d;
}
"""