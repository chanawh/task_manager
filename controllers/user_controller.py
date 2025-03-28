import bcrypt
from models.database import add_user, get_user_by_username

class UserController:
    def __init__(self):
        self.current_user = None

    ### ------------------------ USER AUTHENTICATION ------------------------
    def register_user(self, username, password):
        existing_user = get_user_by_username(username)
        if existing_user:
            return False
        
        # Hash the password before saving
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        add_user(username, hashed_password)
        return True

    def login_user(self, username, password):
        user = get_user_by_username(username)
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):  # No need to call .encode('utf-8') on user[2]
            self.current_user = user
            return user  # Return user object if authentication is successful
        return None

    def logout_user(self):
        self.current_user = None

    def get_current_user(self):
        return self.current_user
