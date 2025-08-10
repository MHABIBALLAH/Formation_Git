import sys
import os

# Add the project root to the Python path.
# This allows us to use absolute imports starting from `src.`, which is a robust practice.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

from src.api.app import create_app  # importer la factory
#from src.api.app import app

if __name__ == '__main__':
    # Running in debug mode is helpful for development.
    # In a real production environment, you would use a proper WSGI server like Gunicorn.
    # Using port 5001 to avoid potential conflicts with other services.
    app.run(host='0.0.0.0', port=5001, debug=True)
