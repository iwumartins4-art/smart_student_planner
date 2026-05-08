# Smart Student Planner

A professional-grade mobile application designed to help university students manage their academic tasks, deadlines, and priorities efficiently. Built with **Kivy** and **KivyMD**, following the **MVVM** architectural pattern.

## 🚀 Features
- **Secure Authentication**: User login and registration with SQLite persistence.
- **Dynamic Dashboard**: Real-time metrics (Today's Tasks, Next Deadline, Completion Rate).
- **Comprehensive Task Management**: Full CRUD operations for academic tasks.
- **Intelligent Filtering**: Fast search bar to find tasks by title, module, or notes.
- **Priority Visualization**: Color-coded indicators for High, Medium, and Low priority tasks.
- **Mobile Optimized**: Material Design 3 UI with responsive layouts and Date Pickers.

## 🛠 Tech Stack
- **Framework**: Kivy 2.3.0
- **UI Library**: KivyMD 2.0.1 (Material Design 3)
- **Language**: Python 3.11+
- **Database**: SQLite3
- **CI/CD**: GitHub Actions (Android APK & iOS builds)

## 📦 Installation & Setup

### Prerequisites
- Python 3.11 or higher
- Git

### Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/supsaveTech/smart_student_planner.git
   cd smart_student_planner
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## ⚠️ Known Limitations
- **Registration Validation**: Currently lacks strict email format verification.
- **Profile Edits**: User profile information (Major, Student ID) is read-only after registration.
- **Testing**: No automated unit test suite is included in this version.
- **Notifications**: Local push notifications for upcoming deadlines are not yet implemented.

## 🔮 Future Improvements
- **Cloud Sync**: Integrate Firebase or AWS for cross-device data synchronization.
- **Calendar View**: A full monthly calendar interface for visual deadline tracking.
- **Push Notifications**: Automated alerts for tasks due within 24 hours.
- **Unit Testing**: Implementation of `pytest` and `Kivy` testing tools to ensure 90%+ code coverage.
- **Dark Mode Toggle**: Allow users to switch between Light and Dark Material themes.
