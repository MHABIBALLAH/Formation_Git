import os
import sys

# Add project root to the Python path to ensure `src` can be found
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.api.app import create_app
from src.api.extensions import db

def main():
    """
    Initializes the database by creating all tables defined in the models.
    This script should be run once to set up the initial database schema.
    """
    app = create_app() # Use the default DevelopmentConfig
    with app.app_context():
        print("Dropping all tables to ensure a clean slate...")
        db.drop_all()
        print("Creating all database tables...")
        db.create_all()
        print("Database tables created successfully.")
        print(f"Database created at: {app.config['SQLALCHEMY_DATABASE_URI']}")


if __name__ == '__main__':
    main()
