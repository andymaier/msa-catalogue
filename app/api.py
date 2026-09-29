"""REST-API (Flask).

TODO (Uebung): Endpunkte implementieren.
Original (Java): GET /articles -> alle Artikel, GET /articles/count -> Anzahl.
"""
from flask import Blueprint, jsonify

from .db import ArticleRepository

bp = Blueprint("articles", __name__)
repo = ArticleRepository()


@bp.get("/articles")
def index():
    # TODO: alle Artikel aus dem Repository als JSON zurueckgeben.
    raise NotImplementedError("GET /articles noch nicht implementiert")


@bp.get("/articles/count")
def count():
    # TODO: Anzahl der Artikel zurueckgeben.
    raise NotImplementedError("GET /articles/count noch nicht implementiert")
