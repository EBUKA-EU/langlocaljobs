# config.py
#
# This file defines the Config class, which holds configuration settings for your Flask app.
# These settings are loaded into the app in app/__init__.py.

import os  # Used to access environment variables


class Config:
    """
    Configuration class for Flask app.
    Reads values from environment variables or uses defaults.
    """
    SECRET_KEY = os.getenv(
        "SECRET_KEY", "dev-secret")  # Secret key for session security
    SQLALCHEMY_DATABASE_URI = os.getenv(
        # Database connection URI (defaults to SQLite)
        "DATABASE_URL", "sqlite:///langlocaljobs.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disables modification tracking for performance
