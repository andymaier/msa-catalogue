"""Datenmodell Article (entspricht der JPA-Entity im Java-Original)."""
from sqlalchemy import Column, String, Numeric
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Article(Base):
    __tablename__ = "article"

    uuid = Column(String, primary_key=True)
    name = Column(String)
    price = Column(Numeric)

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "price": float(self.price) if self.price is not None else None,
        }
