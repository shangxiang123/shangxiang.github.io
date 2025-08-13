from flask import Flask
from flask_cors import CORS

from .config import Settings
from .routes.health import bp as health_bp
from .routes.chat import bp as chat_bp
from .routes.agents import bp as agents_bp


def create_app() -> Flask:
    app = Flask(__name__)
    settings = Settings()
    app.config["SETTINGS"] = settings

    CORS(app, supports_credentials=True)

    app.register_blueprint(health_bp)
    app.register_blueprint(chat_bp, url_prefix="/api")
    app.register_blueprint(agents_bp, url_prefix="/api")

    return app