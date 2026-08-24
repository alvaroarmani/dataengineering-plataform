"""Fixtures compartilhadas para exercícios do TRACK REAL (bancada Docker).

Conecta no Postgres da bancada usando as variáveis de ambiente do docker-compose.
Rode DENTRO da bancada (o container Jupyter já enxerga o host `postgres`), ou
localmente com o Postgres exposto em localhost:5432.

    # na raiz do repo, com a bancada de pé (docker compose up -d):
    pip install psycopg2-binary pytest
    pytest -q modulos/NN-modulo/exercicio-XX

Variáveis (com defaults do .env.example): POSTGRES_HOST, POSTGRES_PORT,
POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB.
"""
import os

import pytest

try:
    import psycopg2
except ModuleNotFoundError:  # ajuda quem esqueceu de instalar
    psycopg2 = None


def _dsn():
    return dict(
        host=os.environ.get("POSTGRES_HOST", "localhost"),
        port=int(os.environ.get("POSTGRES_PORT", "5432")),
        user=os.environ.get("POSTGRES_USER", "curso"),
        password=os.environ.get("POSTGRES_PASSWORD", "curso"),
        dbname=os.environ.get("POSTGRES_DB", "curso"),
    )


@pytest.fixture
def pg():
    """Conexão limpa com o Postgres da bancada; faz rollback ao final (não suja o banco)."""
    if psycopg2 is None:
        pytest.skip("psycopg2 não instalado — rode na bancada (pip install psycopg2-binary).")
    try:
        conn = psycopg2.connect(**_dsn())
    except Exception as e:  # noqa: BLE001
        pytest.skip(f"Postgres indisponível ({e}). Suba a bancada: docker compose up -d.")
    conn.autocommit = False
    try:
        yield conn
    finally:
        conn.rollback()
        conn.close()
