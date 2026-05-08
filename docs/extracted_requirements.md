# PART 1: Extracted Requirements (LDC6004M)

The following requirements have been extracted from the Assessment Brief for **LDC6004M: Mobile Application Development**, specifying the criteria for the "Smart Student Planner" project.

## 1. Core Feature Requirements
*   **Authentication System**: Secure Login and Logout functionality.
*   **Dashboard**: A centralized screen displaying a summary of academic tasks and metrics.
*   **Task Management (CRUD)**:
    *   **Add**: Ability to create new academic tasks with titles, modules, and deadlines.
    *   **Edit**: Modify existing task details.
    *   **Delete**: Remove obsolete or incorrect tasks.
    *   **Complete**: Mark tasks as "Completed" (Binary state or status update).
    *   **Search**: Filter tasks by keyword, title, or module.

## 2. Functional Requirements
*   **Multi-Screen Navigation**: Smooth transitions between Login, Dashboard, Task Forms, and Settings/Profile screens.
*   **User Input Handling**: Professional handling of text input, dropdown selections, and date picking.
*   **Local Data Persistence**: Implementation of a local database (e.g., SQLite) to ensure data persists across app restarts.
*   **State Management**: Real-time updates of the UI when underlying data changes (e.g., list updates after saving).
*   **Validation**: Client-side validation to prevent empty titles or invalid dates.
*   **Responsive UI**: The layout must adapt to various mobile screen orientations and sizes.

## 3. Technical Expectations
*   **Architecture**: Mandatory use of a recognized architectural pattern (MVC, MVP, or **MVVM**).
*   **Code Quality**: Adherence to PEP 8 (for Python) or relevant language standards; use of modular, DRY (Don't Repeat Yourself) code.
*   **Testing**: Basic verification of functionality (unit or manual testing evidence).
*   **Version Control**: Consistent use of Git for change tracking, with descriptive commit messages.

## 4. Portfolio Artefacts (Submission Requirements)
*   **Source Code**: Fully functional codebase.
*   **Design Documentation**: Clear explanation of the app purpose, wireframes, and architecture.
*   **Screenshots**: Visual evidence of all core functionalities.
*   **README**: Professional project overview and setup instructions.

## 5. Marking Criteria (Critical Alignment)
| Category | Weighting/Expectation |
| :--- | :--- |
| **UI Design** | Professional use of Material Design, consistent spacing, and readable typography. |
| **Navigation** | Intuitive flow; use of standardized navigation patterns (AppBars, FABs). |
| **Data Integrity** | Correct implementation of SQL schemas and data types. |
| **State & Logic** | Separation of business logic from UI code (Model/ViewModel separation). |
| **Professionalism** | Evidence of version control (Git) and automated workflows (CI/CD). |
| **Completeness** | All core features fully operational without crashes. |
