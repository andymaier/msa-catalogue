import json
import threading
from dataclasses import dataclass
from typing import Any

from confluent_kafka import Consumer, Producer, KafkaException

from .config import KAFKA_BOOTSTRAP_SERVERS, SHOP_TOPIC, KAFKA_GROUP_ID
from .db import ArticleRepository


@dataclass
class Operation:
    bo: str
    action: str
    object: Any = None

    @staticmethod
    def from_bytes(raw: bytes) -> "Operation":
        d = json.loads(raw.decode("utf-8"))
        return Operation(d.get("bo"), d.get("action"), d.get("object"))

    def to_bytes(self) -> bytes:
        return json.dumps(
            {"bo": self.bo, "action": self.action, "object": self.object}
        ).encode("utf-8")


class ShopProducer:
    """Sendet Operation-Events auf 'shop' (confluent-kafka). Verbindung wird
    verzoegert aufgebaut, damit die App auch ohne laufendes Kafka startet."""

    def __init__(self):
        self._producer = None

    def _get(self):
        if self._producer is None:
            self._producer = Producer({"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS})
        return self._producer

    def send(self, op: "Operation"):
        errors = []

        def _cb(err, msg):
            if err is not None:
                errors.append(err)

        p = self._get()
        p.produce(SHOP_TOPIC, value=op.to_bytes(), on_delivery=_cb)
        p.flush(10)
        if errors:
            raise KafkaException(errors[0])


class ShopListener:
    def __init__(self, repo: ArticleRepository):
        self.repo = repo

    def handle(self, op: Operation):
        # TODO: Operation verarbeiten.
        #   - nur Events mit bo == "article" sind relevant
        #   - action "create"/"update" -> Artikel per repo.save(op.object) anlegen/aktualisieren
        #   - action "delete"          -> Artikel per repo.delete(...) entfernen
        raise NotImplementedError("ShopListener.handle noch nicht implementiert")

    def start(self):
        threading.Thread(target=self._consume, daemon=True).start()

    def _consume(self):
        consumer = Consumer(
            {
                "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
                "group.id": KAFKA_GROUP_ID,
                "auto.offset.reset": "earliest",
            }
        )
        consumer.subscribe([SHOP_TOPIC])
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"[catalogue] Consumer-Fehler: {msg.error()}")
                continue
            try:
                self.handle(Operation.from_bytes(msg.value()))
            except Exception as e:
                print(f"[catalogue] Fehler beim Verarbeiten: {e}")
