"""Postgres-Anbindung + Repository (Pendant zu Spring-Data ArticleRepository).

Der Repository-Teil ist VOLLSTAENDIG vorgegeben - er ist nicht Teil der
Uebung. Zu implementieren sind API (app/api.py) und Kafka-Listener
(app/events.py)."""
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from .config import DATABASE_URL
from .models import Base, Article

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, future=True)


def init_db():
    """Legt die Tabelle an, falls sie fehlt (entspricht ddl-auto: update)."""
    Base.metadata.create_all(engine)


class ArticleRepository:
    def find_all(self):
        with SessionLocal() as s:
            return [a.to_dict() for a in s.query(Article).all()]

    def count(self):
        with SessionLocal() as s:
            return s.query(func.count(Article.uuid)).scalar()

    def find_by_id(self, uuid):
        with SessionLocal() as s:
            a = s.get(Article, uuid)
            return a.to_dict() if a else None

    def save(self, data: dict):
        """Upsert. Nur nicht-null Felder werden uebernommen
        (entspricht NullAwareBeanUtilsBean im Original)."""
        with SessionLocal() as s:
            a = s.get(Article, data["uuid"])
            if a is None:
                a = Article(uuid=data["uuid"])
                s.add(a)
            if data.get("name") is not None:
                a.name = data["name"]
            if data.get("price") is not None:
                a.price = data["price"]
            s.commit()

    def delete(self, uuid):
        with SessionLocal() as s:
            a = s.get(Article, uuid)
            if a:
                s.delete(a)
                s.commit()
