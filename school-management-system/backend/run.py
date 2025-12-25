import sys
from os.path import dirname, abspath

# Add the backend directory to the Python path
sys.path.insert(0, dirname(abspath(__file__)))

from app import create_app  # Ensure this imports from app/__init__.py

app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)  # Updated port to 5001
