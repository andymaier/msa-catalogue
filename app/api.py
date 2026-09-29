"""REST-API (Flask) - Loesung."""
from flask import Blueprint, jsonify

from .db import ArticleRepository

bp = Blueprint("articles", __name__)
repo = ArticleRepository()


@bp.get("/articles")
def index():
    return jsonify(repo.find_all())


@bp.get("/articles/count")
def count():
    return jsonify(repo.count())
