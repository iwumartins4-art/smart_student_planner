# Smart Student Planner - Design Documentation

## 1. App Purpose and Target Users
The **Smart Student Planner** is a high-productivity mobile application designed specifically for students in higher education. Its primary goal is to centralize academic tasks, deadlines, and module-specific notes into a single, intuitive interface.

**Target Users:**
- University students managing multiple course modules.
- Distance learners needing strict deadline tracking.
- Any student looking to improve time management through a "Smart" digital planner.

## 2. Architecture Overview (MVVM)
To ensure the code is maintainable, scalable, and follows professional development standards, the application implements the **Model-View-ViewModel (MVVM)** design pattern.

### Why MVVM?
- **Separation of Concerns**: UI code (Kivy) is entirely decoupled from business logic and database management.
- **Data Binding**: Kivy's property system acts as the binder between the View and ViewModel.
- **Testability**: Business logic in ViewModels can be tested independently of the graphical user interface.

### Architecture Breakdown:
```mermaid
graph TD
    subgraph View_Layer
        V1[LoginView.kv]
        V2[DashboardView.kv]
        V3[TaskFormView.kv]
    end

    subgraph ViewModel_Layer
        VM1[AuthViewModel.py]
        VM2[TaskViewModel.py]
    end

    subgraph Model_Layer
        M1[Database.py - SQLite]
    end

    View_Layer -->|User Interactions| ViewModel_Layer
    ViewModel_Layer -->|Data Updates| View_Layer
    ViewModel_Layer -->|Queries/CRUD| Model_Layer
    Model_Layer -->|Raw Data| ViewModel_Layer
```

## 3. Navigation Flow Diagram
The application follows a simple, secure, and user-friendly navigation flow.

```mermaid
stateDiagram-v2
    [*] --> Login: Start App
    Login --> Dashboard: Valid Credentials
    Dashboard --> TaskForm: Create New Task (FAB)
    Dashboard --> TaskForm: Edit Existing Task (Click Item)
    TaskForm --> Dashboard: Save / Cancel
    Dashboard --> Login: Logout
```

## 4. Technical Implementation
- **Framework**: Kivy + KivyMD (Targeting Android/iOS).
- **Persistence**: SQLite (Local SQL database for data integrity).
- **Styling**: Material Design 3 (Deep Purple theme).
- **Validation**: All form inputs are validated in the `TaskViewModel` before persistence.
