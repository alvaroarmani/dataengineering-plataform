"""Fixture `pg` — Postgres da bancada (track real). Skip fora da bancada."""
import os

import pytest

try:
    import psycopg2
except ModuleNotFoundError:
    psycopg2 = None


@pytest.fixture
def pg():
    if psycopg2 is None:
        pytest.skip("psycopg2 não instalado — rode na bancada (pip install psycopg2-binary).")
    try:
        conn = psycopg2.connect(
            host=os.environ.get("POSTGRES_HOST", "localhost"),
            port=int(os.environ.get("POSTGRES_PORT", "5432")),
            user=os.environ.get("POSTGRES_USER", "curso"),
            password=os.environ.get("POSTGRES_PASSWORD", "curso"),
            dbname=os.environ.get("POSTGRES_DB", "curso"),
        )
    except Exception as e:  # noqa: BLE001
        pytest.skip(f"Postgres indisponível ({e}). Suba a bancada: docker compose up -d.")
    conn.autocommit = False
    try:
        yield conn
    finally:
        conn.rollback()
        conn.close()
