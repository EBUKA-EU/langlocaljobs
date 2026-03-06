# run.py
#
# This is the main entrypoint for your Flask application.
# It creates the app instance using the factory function and starts the development server.
#
# Usage: Run this file directly to start the backend server.

from app import create_app  # Import the app factory function

app = create_app()  # Create the Flask app instance

if __name__ == "__main__":
    # Only run the server if this script is executed directly (not imported)
    app.run(debug=True)  # Start the Flask development server with debug mode enabled
