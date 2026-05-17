# Smart Student Planner

A professional-grade, cross-platform mobile and desktop application designed specifically for university students. The Smart Student Planner provides a centralized hub for managing academic tasks, tracking deadlines, and monitoring course progress with a stunning Material Design 3 interface.

Built with **Python 3.11.5**, **Kivy**, and **KivyMD**, the application follows the **MVVM** (Model-View-ViewModel) architectural pattern to ensure code maintainability, stability, and scalability.

## 🚀 Key Features

- **Personalized Dashboard**: A high-impact overview featuring real-time metrics for "Today's Tasks," "Next Deadline" (with intelligent countdowns), and "Weekly Goal" progress.
- **Advanced Task Management**: Full CRUD (Create, Read, Update, Delete) operations for tasks, including module association, priority levels, and custom notes.
- **Smart Search & Filtering**: An integrated live-search bar that filters tasks instantly as you type, supporting module and title matching.
- **Premium Material 3 UI**: A sleek Dark Mode interface utilizing custom-drawn components for maximum rendering stability on Windows, Linux, and Mobile.
- **Secure Data Persistence**: Local SQLite3 database integration ensures your data stays safe and private on your device.
- **Priority Visualization**: Color-coded indicators (Red/Orange/Green) for immediate visual identification of task urgency.
- **Profile Management**: Dedicated user profile page displaying registration details and academic major.

## 🛠 Tech Stack

- **Core**: Python 3.11.5 (Required for optimal stability)
- **Framework**: Kivy 2.3.1
- **UI Library**: KivyMD 2.0.1 (Material Design 3 Certified)
- **Database**: SQLite3
- **Graphics Backend**: Forced ANGLE (OpenGL ES 2.0) on Windows for maximum compatibility with Intel Iris Xe and other modern GPUs.

## 📦 Installation & Setup

To ensure a smooth installation, please follow these steps exactly.

### 1. Prerequisites
- **[Python 3.11.5 - Windows installer (64-bit)](https://www.python.org/downloads/release/python-3115/)**: This is the required version.
Ensure you check the **Add python.exe to PATH** box during installation.

- **[Git for Windows](https://git-scm.com/install/windows)**: Installed and configured.

### 💻 Standalone Executable (.exe) for Windows (No Setup Required)

If you want to run and test the application instantly without installing Python or setting up a virtual environment:
1. Navigate to the **Actions** tab of this repository on GitHub.
2. Click on the most recent successful run of the **Build Windows EXE** workflow.
3. Scroll down to the **Artifacts** section at the bottom.
4. Download the `SmartStudentPlanner-Windows-EXE` zip file, extract it, and double-click `SmartStudentPlanner.exe` to run the app immediately!

### 2. Windows Installation (Developer Setup)

1.  **Clone the Repository**:
    ```powershell
    git clone https://github.com/iwumartins4-art/smart_student_planner
    cd smart_student_planner
    ```

2.  **Create a Virtual Environment**:
    ```powershell
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Upgrade Pip & Install Dependencies**:
    ```powershell
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

4.  **Run the Application**:
    ```powershell
    python main.py
    ```

## ⚠️ Stability Notes for Windows Users

The application is configured to automatically handle common Windows graphics crashes by forcing the `ANGLE` backend. If you encounter any visual glitches:
- Ensure your GPU drivers are up to date.
- The app logs detailed startup information to `app_startup.log` in the root directory.

---
**Developed by Martins Chinatu Iwu (iwumartins4-art) for the Smart Student Community.**