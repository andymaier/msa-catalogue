# msa-catalogue (Python)

Python-Portierung des Java/Spring-Boot-Service `catalogue` aus dem
predic8-MSA-Shop. Flask (REST) + confluent-kafka (Event-Anbindung) + PostgreSQL.

## Architektur
- REST `GET /articles`, `GET /articles/count` (nur lesend).
- Kafka-Topic `shop`, Nachricht `Operation {bo, action, object}`.
  Der Service **hoert** auf `shop` und pflegt seinen Artikel-Store
  (create/update/delete) anhand der Events.

## Branches
- `main`     – Skelett; **API (`app/api.py`) und Kafka-Listener
  (`app/events.py`) sind als TODO offen** (Uebungsstand).
- `solution` – fertige Loesung.

## Start
    python3 -m venv .venv && . .venv/bin/activate
    pip install -r requirements.txt
    # Postgres + Kafka muessen laufen (Defaults: localhost:5432 / localhost:9092)
    python -m app.main

Konfiguration ueber Env-Vars: `DATABASE_URL`, `KAFKA_BOOTSTRAP_SERVERS`,
`SHOP_TOPIC`, `KAFKA_GROUP_ID`, `SERVER_PORT`.
