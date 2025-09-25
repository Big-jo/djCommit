# This is a larger change that should trigger "good" classification
# It has more than 10 lines of changes

class UserService:
    def __init__(self):
        self.users = {}
        self.active_sessions = set()
    
    def create_user(self, username, email):
        """Create a new user account."""
        if username in self.users:
            raise ValueError("Username already exists")
        
        user = {
            'username': username,
            'email': email,
            'created_at': datetime.now(),
            'is_active': True
        }
        
        self.users[username] = user
        return user
    
    def authenticate_user(self, username, password):
        """Authenticate a user with username and password."""
        if username not in self.users:
            return False
        
        user = self.users[username]
        if not user['is_active']:
            return False
        
        # In a real implementation, you'd hash and compare passwords
        return True
    
    def deactivate_user(self, username):
        """Deactivate a user account."""
        if username in self.users:
            self.users[username]['is_active'] = False
            return True
        return False

# Additional utility functions
def validate_email(email):
    """Basic email validation."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def generate_user_id():
    """Generate a unique user ID."""
    import uuid
    return str(uuid.uuid4())
