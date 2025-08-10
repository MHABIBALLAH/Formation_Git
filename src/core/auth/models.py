from flask_login import UserMixin
from src.api.extensions import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    """Flask-Login hook to load a user by ID."""
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """User model for authentication and authorization."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(80), nullable=False, default='user')

    def __repr__(self):
        return f"<User {self.username}>"
