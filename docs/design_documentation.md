# PART 3: Design Documentation

## 1. App Purpose and Target Users
The **Smart Student Planner** is a specialized task management tool built for university students to manage academic workloads. It addresses the complexity of tracking multiple course modules, varying priorities, and strict deadlines.

**Target Users:**
*   **Full-time Students**: Managing 4-6 modules simultaneously.
*   **Postgraduate Researchers**: Tracking long-term project milestones.
*   **Commuter Students**: Needing offline access to their schedule via local persistence.

## 2. Wireframes (Text-Based Descriptions)

### Screen A: Login / Register
*   **Header**: App Logo (`assets/logo.png`) and "Smart Student Planner" title.
*   **Inputs**: Outlined text fields for Username and Password.
*   **Actions**: "LOGIN" button (primary), "REGISTER" button (text-style).
*   **Validation**: Error text appears below fields for invalid credentials.

### Screen B: Dashboard
*   **AppBar**: Small top bar with Settings, Profile, and Logout icons.
*   **Greeting**: "Hi, [Username]!" with a summary label.
*   **Metrics Row**: Three cards showing "Today's Tasks", "Next Deadline", and "Weekly Goal %".
*   **Task List**: Vertical scrolling list of `TaskCards`.
*   **Task Card**: Shows Priority (Left color bar), Title (Strikethrough if completed), Module, and Status chip.
*   **Action**: Floating Action Button (+) for adding tasks.

### Screen C: Task Form (Add/Edit)
*   **AppBar**: "Add Task" or "Edit Task" title with a back arrow.
*   **Form**: Outlined fields for Title, Module, Due Date (Calendar icon), Priority (Dropdown), and Notes.
*   **Action**: Full-width "SAVE TASK" button at the bottom.

## 3. Navigation Flow
1.  **Entry**: App starts at `LoginView`.
2.  **Auth**: Successful login redirects to `DashboardView`.
3.  **Task Creation**: Clicking the FAB in Dashboard opens `TaskFormView` (Add mode).
4.  **Task Modification**: Clicking a task card in Dashboard opens `TaskFormView` (Edit mode).
5.  **Settings/User**: Toolbar icons lead to `SettingsView` or `UserView`.
6.  **Exit**: Logout button returns user to `LoginView`.

## 4. Architecture Overview (MVVM)
The app implements the **Model-View-ViewModel** pattern to ensure clean separation of UI and business logic.

*   **View (Kivy/KV)**: `login_view.kv`, `dashboard_view.kv`. Purely declarative UI.
*   **ViewModel (Python)**: `auth_viewmodel.py`, `task_viewmodel.py`. Contains all logic for filtering, mapping data for display, and triggering DB operations.
*   **Model (SQLite)**: `database.py`. Singleton class managing raw SQL queries and data integrity.

### Data Flow Example (Search):
1.  User types in `MDTextField` (View).
2.  `DashboardView` calls `TaskViewModel.get_tasks(query)` (ViewModel).
3.  ViewModel calls `Database.get_all_tasks(query)` (Model).
4.  Model returns raw tuples.
5.  ViewModel transforms tuples into a list of dictionaries.
6.  View's `RecycleView` binds to this list and updates automatically.
