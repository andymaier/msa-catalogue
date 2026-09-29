"""Zentrale Konfiguration. Alles per Umgebungsvariable ueberschreibbar,
Defaults entsprechen dem urspruenglichen Java-Service (application.yml)."""
import os

# PostgreSQL wie im Java-Original: jdbc:postgresql://localhost:5432/catalogue
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://catalogue:catalogue@localhost:5432/catalogue",
)

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
SHOP_TOPIC = os.getenv("SHOP_TOPIC", "shop")
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID", "catalogue-1")

SERVER_PORT = int(os.getenv("SERVER_PORT", "8080"))
