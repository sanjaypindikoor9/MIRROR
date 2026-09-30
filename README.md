# MIRROR — Intelligent Digital Workspace Assistant

MIRROR is an AI-powered desktop workspace assistant designed to understand a user's digital activity and provide contextual assistance.

## Features

* 🖥️ **Screen Context Detection** — Captures and analyzes the active application and screen context.
* 👁️ **OCR-Based Perception** — Extracts useful text information from the screen.
* 🧠 **Context Intelligence** — Understands the user's current workspace and activity.
* 📋 **Activity Tracking** — Tracks application usage and workspace activity.
* 🎯 **Task Detection** — Identifies tasks and activities from the user's digital context.
* 🗂️ **Workspace Management** — Organizes activity based on the user's current workflow.
* 💾 **Local Storage** — Stores workspace and activity information locally.
* 🖥️ **Desktop Dashboard** — Provides a visual interface for interacting with MIRROR.

## Project Structure

```text
MIRROR/
├── app/
│   ├── capture/
│   ├── intelligence/
│   ├── perception/
│   ├── planner/
│   ├── storage/
│   └── ui/
├── data/
├── .vscode/
├── .gitignore
└── run.py
```

## Technologies Used

* Python
* PySide6
* OCR
* SQLite
* Computer Vision
* AI/ML-based Context Analysis

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/sanjaypindikoor9/MIRROR.git
cd MIRROR
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run MIRROR

```bash
python run.py
```

## Note

MIRROR is a prototype focused on intelligent desktop context awareness, activity understanding, and workspace assistance.

## Author

**Sanjay Pindikoor**
