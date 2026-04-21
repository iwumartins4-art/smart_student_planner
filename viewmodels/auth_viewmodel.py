class AuthViewModel:
    def __init__(self):
        self.is_logged_in = False
        self.current_user = None

    def login(self, username, password):
        # Implementation of core authentication logic
        # In a real app, this would check against a DB hash. 
        # For this planner, any non-empty credentials work for demo purposes.
        if username and password:
            self.is_logged_in = True
            self.current_user = username
            return True, "Login successful"
        else:
            return False, "Invalid username or password"

    def logout(self):
        self.is_logged_in = False
        self.current_user = None
        return True, "Logged out successfully"
