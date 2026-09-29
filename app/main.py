"""Anwendungs-Einstiegspunkt: Flask-App + Kafka-Consumer-Thread."""
from flask import Flask

from .config import SERVER_PORT
from .db import init_db, ArticleRepository
from .events import ShopListener
from .api import bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(bp)
    init_db()
    ShopListener(ArticleRepository()).start()
    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=SERVER_PORT)
