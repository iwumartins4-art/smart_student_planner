# Smart Student Planner

A premium, cross-platform mobile application designed to help students manage their academic tasks effectively. Built with **KivyMD (Material Design 3)** and following strict **MVVM architecture**.

## ✨ Features
- **Secure Authentication**: User registration and login flow.
- **Smart Dashboard**: High-contrast, dynamic overview of academic tasks.
- **Task Management**: Full CRUD operations with priority levels (Low, Medium, High).
- **Advanced Search**: Real-time filtering by module name or task title.
- **High Contrast UI**: Optimized dark and light mode color mapping for maximum legibility.
- **Reliable Persistence**: SQLite backend ensuring data safety.
- **Automated CI/CD**: Cloud-based pipeline generating Android (`.apk`) and iOS (`.xcodeproj`) builds automatically on push.

## 🛠️ Frameworks & Tools
- **Language**: Python 3.11+
- **UI Framework**: Kivy (`2.3.1`) & KivyMD (`2.0.1.dev0`)
- **Database**: SQLite3
- **Architecture**: MVVM (Model-View-ViewModel)
- **CI/CD**: GitHub Actions (Buildozer for Android, Native Kivy-iOS toolchain for iOS)

## 🚀 Installation & Local Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/supsaveTech/smart_student_planner
   cd smart_student_planner
   ```

2. **Install dependencies**:
   ```bash
   pip install kivy
   pip install https://github.com/kivymd/KivyMD/archive/master.zip
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## 🏗️ Deployment Pipelines

The repository features fully automated GitHub Actions workflows:
- **Android (`.github/workflows/android.yml`)**: Uses Ubuntu runners and `buildozer` to seamlessly package the application into a production-ready `.apk`.
- **iOS (`.github/workflows/ios.yml`)**: Uses macOS runners and a direct Kivy-iOS `toolchain.py` strategy to compile an Apple `.xcodeproj`. 
  - *Note: To sidestep KivyMD `pycairo` cross-compilation errors on iOS, the workflow programmatically strips non-essential dependencies and dynamically bundles pure-Python libraries.*

## 📝 Design Decisions
- **SQLite vs JSON**: SQLite was chosen for its atomic properties and relational structure, ensuring better data integrity for a "Student" application where loss of assignment data is critical.
- **MVVM Integration**: Implementing MVVM completely removes the "God Object" anti-pattern in Kivy, separating UI styling (`.kv`) from logic (`.py`).
- **Native iOS Compilation**: Bypassed Buildozer for iOS in favor of the native Kivy-iOS toolchain to ensure reliable compilation and prevent legacy `ios-deploy` crashes on CI servers.

## ⚠️ Known Limitations & Future Enhancements
- **Limitations**:
  - The generated iOS Xcode project hardcodes absolute paths to the GitHub Action runner environment. To deploy the `.ipa` locally, `toolchain.py` must be run on the host Mac.
- **Future Enhancements**: 
  - Google Calendar API Integration.
  - Push notifications for approaching deadlines.
  - Cloud database synchronization (Firebase/Supabase) for multi-device support.
