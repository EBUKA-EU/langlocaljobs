from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.extension import db, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)

    @app.get("/api/health")
    def health():
        return {"status": "Backend healthy"}

    return app
