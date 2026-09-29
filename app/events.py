"""Kafka-Anbindung: Operation-Event, Producer und ShopListener.

TODO (Uebung): den Listener implementieren - die Verarbeitung eines
Operation-Events und die Pflege des Artikel-Stores.
"""
import json
import threading
from dataclasses import dataclass
from typing import Any

from kafka import KafkaConsumer, KafkaProducer

from .config import KAFKA_BOOTSTRAP_SERVERS, SHOP_TOPIC, KAFKA_GROUP_ID
from .db import ArticleRepository


@dataclass
class Operation:
    """Event-Nachricht auf dem Topic 'shop' (wie im Java-Original)."""
    bo: str            # Business-Objekt, z.B. "article"
    action: str        # "create" | "update" | "delete"
    object: Any = None # Nutzdaten als dict

    @staticmethod
    def from_bytes(raw: bytes) -> "Operation":
        d = json.loads(raw.decode("utf-8"))
        return Operation(d.get("bo"), d.get("action"), d.get("object"))

    def to_bytes(self) -> bytes:
        return json.dumps(
            {"bo": self.bo, "action": self.action, "object": self.object}
        ).encode("utf-8")


class ShopProducer:
    """Sendet Operation-Events auf das Topic 'shop' (vorgegeben)."""

    def __init__(self):
        self._producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda op: op.to_bytes(),
        )

    def send(self, op: Operation):
        self._producer.send(SHOP_TOPIC, op).get(timeout=10)


class ShopListener:
    """Konsumiert Events vom Topic 'shop' und pflegt den Artikel-Store."""

    def __init__(self, repo: ArticleRepository):
        self.repo = repo

    def handle(self, op: Operation):
        # TODO: Operation verarbeiten.
        #   - nur Events mit bo == "article" sind relevant
        #   - action "create"/"update" -> Artikel per repo.save(op.object) anlegen/aktualisieren
        #   - action "delete"          -> Artikel per repo.delete(...) entfernen
        raise NotImplementedError("ShopListener.handle noch nicht implementiert")

    def start(self):
        """Startet den Consumer in einem Hintergrund-Thread."""
        threading.Thread(target=self._consume, daemon=True).start()

    def _consume(self):
        consumer = KafkaConsumer(
            SHOP_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            group_id=KAFKA_GROUP_ID,
            auto_offset_reset="earliest",
            value_deserializer=Operation.from_bytes,
        )
        for msg in consumer:
            try:
                self.handle(msg.value)
            except Exception as e:  # im Uebungsstand erwartet (TODO)
                print(f"[catalogue] Fehler beim Verarbeiten: {e}")
