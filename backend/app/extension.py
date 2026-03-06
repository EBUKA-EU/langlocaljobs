# extension.py
#
# This file initializes and exports the database (db) and migration (migrate) extensions for use in the Flask app.
# These are imported and initialized in app/__init__.py.

from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy ORM for database operations
from flask_migrate import Migrate        # Flask-Migrate for handling migrations

db = SQLAlchemy()  # The database object, used to define models and interact with the database
migrate = Migrate()  # The migration object, used to manage database schema changes
