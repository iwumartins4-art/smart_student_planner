# Smart Student Planner

A premium, cross-platform mobile application designed to help students manage their academic tasks effectively. Built with **KivyMD (Material Design 3)** and following strict **MVVM architecture**.

## ✨ Features
- **Secure Authentication**: Robust user registration and login flow with database-backed verification.
- **Smart Dashboard**: High-contrast progress card showing real-time task completion statistics.
- **Task Management**: Full CRUD operations with priority levels (Low, Medium, High) and delete confirmation.
- **User Profile**: Dedicated profile view displaying student name, ID, major, and email.
- **Advanced Search**: Real-time filtering with a clean, compact search bar and empty-state feedback.
- **High Contrast UI**: Premium Material 3 design optimized for both dark and light modes.
- **Reliable Persistence**: SQLite backend ensuring academic data is never lost.
- **Automated CI/CD**: Fully automated pipeline generating Android (`.apk`) builds on every push.

## 🛠️ Frameworks & Tools
- **Language**: Python 3.11+
- **UI Framework**: Kivy (`2.3.1`) & KivyMD (`2.0.1.dev0`)
- **Database**: SQLite3
- **Architecture**: MVVM (Model-View-ViewModel)
- **CI/CD**: GitHub Actions (Buildozer for Android, Native Kivy-iOS toolchain for iOS)

## 🚀 Installation & Local Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/iwumartins4-art/smart_student_planner
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

## 📥 Downloading & Installing Artifacts

When a commit is pushed, GitHub Actions will compile the app and generate downloadable artifacts.

### 🤖 Android (.apk)
1. Go to the **[Actions](../../actions)** tab of this repository.
2. Click on the latest successful **Android Build** run.
3. Scroll to the bottom under **Artifacts** and download `SmartStudentPlanner-APK`.
4. Transfer the `.apk` file to your Android device.
5. Open the file on your device (ensure "Install from Unknown Sources" is enabled in settings) to install.

### 🍏 Apple iOS (.xcodeproj)
1. Go to the **[Actions](../../actions)** tab of this repository.
2. Click on the latest successful **iOS Build** run.
3. Scroll to the bottom under **Artifacts** and download `ios-xcode-project`.
4. **Important macOS Requirement**: Apple restricts iOS compilation to macOS environments. Because Kivy-iOS compiles libraries using absolute paths on the cloud runner, you must reconstruct the paths locally on a Mac device to deploy the `.ipa` via Xcode.
   - Extract the source code to your local macOS device.
   - Clone Kivy-iOS: `git clone https://github.com/kivy/kivy-ios.git`
   - Build the libraries locally: `python3 toolchain.py build python3 kivy pillow`
   - Create the project: `python3 toolchain.py create "SmartStudentPlanner" <path_to_source>`
   - Open the generated Xcode project locally and deploy to your iPhone!

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
# smart_student_planner
