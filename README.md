# Smart Student Planner

A premium, cross-platform mobile application designed to help students manage their academic tasks effectively. Built with **KivyMD** and following strict **MVVM architecture**.

## ✨ Features
- **Secure Authentication**: Simple login/logout system.
- **Smart Dashboard**: Overview of all academic tasks with modern cards.
- **Task Management**: Full CRUD (Create, Read, Update, Delete) for student tasks.
- **Advanced Search**: Real-time filtering by module name or task title.
- **Reliable Persistence**: SQLite backend ensuring data safety.
- **Premium UI**: "Smart" Deep Purple high-end theme with responsive layouts.

## 🛠️ Frameworks & Tools
- **Language**: Python 3.13
- **UI Framework**: Kivy & KivyMD (Material Design 3)
- **Database**: SQLite3
- **Architecture**: MVVM (Model-View-ViewModel)

## 🚀 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd smart_student_planner
   ```

2. **Install dependencies**:
   ```bash
   pip install kivy kivymd
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## 📝 Design Decisions
- **SQLite vs JSON**: SQLite was chosen for its atomic properties and relational structure, ensuring better data integrity for a "Student" application where loss of assignment data is critical.
- **MVVM**: Implementing MVVM avoids the "God Object" anti-pattern in Kivy, separating UI styling (.kv) from logic (.py).

## ⚠️ Known Limitations & Future Enhancements
- **Limitations**: Currently supports local storage only; search is keyword-based.
- **Future Enhancements**: 
    - Integration with Google Calendar API.
    - Push notifications for upcoming deadlines.
    - Cloud synchronization for multi-device support.
