# __init__.py
#
# This is the application factory for your Flask project.
# It creates and configures the Flask app, sets up extensions, and registers routes.
#
# Usage: Imported by run.py to create the app instance.

from flask import Flask  # Flask web framework
from flask_cors import CORS  # Cross-Origin Resource Sharing for APIs
from app.config import Config  # App configuration settings
from app.extension import db, migrate  # Database and migration extensions


def create_app():
    """
    Application factory function. Creates and configures the Flask app instance.
    """
    app = Flask(__name__)
    app.config.from_object(Config)  # Load configuration from Config class

    CORS(app)  # Enable CORS for all routes

    db.init_app(app)  # Initialize SQLAlchemy with app
    migrate.init_app(app, db)  # Initialize Flask-Migrate with app and db

    @app.get("/api/health")
    def health():
        """Health check endpoint to verify backend is running."""
        return {"status": "Backend healthy"}

    return app
