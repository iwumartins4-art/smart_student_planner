from models.database import Database

class AuthViewModel:
    def __init__(self):
        self.db = Database()
        self.is_logged_in = False
        self.current_user_data = None

    def login(self, username, password):
        user = self.db.authenticate_user(username, password)
        if user:
            self.is_logged_in = True
            # user tuple: (id, full_name, username, email, password, major, student_id)
            self.current_user_data = {
                "id": user[0],
                "full_name": user[1],
                "username": user[2],
                "email": user[3],
                "major": user[5],
                "student_id": user[6]
            }
            return True, "Login successful"
        else:
            return False, "Invalid username or password"

    def register(self, full_name, username, email, password, major, student_id):
        return self.db.add_user(full_name, username, email, password, major, student_id)

    def logout(self):
        self.is_logged_in = False
        self.current_user_data = None
        return True, "Logged out successfully"
