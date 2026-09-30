import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import parse_imagem, reprodutivel  # noqa: E402


@pytest.mark.parametrize("ref, esperado", [
    ("postgres", {"registry": "docker.io", "repositorio": "library/postgres", "tag": "latest", "digest": None}),
    ("postgres:16", {"registry": "docker.io", "repositorio": "library/postgres", "tag": "16", "digest": None}),
    ("apache/airflow:2.9.3", {"registry": "docker.io", "repositorio": "apache/airflow", "tag": "2.9.3", "digest": None}),
    ("ghcr.io/dbt-labs/dbt-postgres:1.8.2",
     {"registry": "ghcr.io", "repositorio": "dbt-labs/dbt-postgres", "tag": "1.8.2", "digest": None}),
    ("localhost:5000/etl", {"registry": "localhost:5000", "repositorio": "etl", "tag": "latest", "digest": None}),
    ("localhost:5000/etl@sha256:ab12", {"registry": "localhost:5000", "repositorio": "etl", "tag": None,
                                        "digest": "sha256:ab12"}),
])
def test_parse(ref, esperado):
    assert parse_imagem(ref) == esperado


@pytest.mark.parametrize("ref, nivel", [
    ("postgres", "flutuante"), ("postgres:16", "flutuante"), ("python:3.12-slim", "versao"),
    ("postgres:16.4", "versao"), ("etl@sha256:ab12", "digest"),
])
def test_reprodutivel(ref, nivel):
    assert reprodutivel(ref) == nivel


def test_invalidas():
    for ref in ["", "Postgres:16", "minha imagem"]:
        with pytest.raises(ValueError):
            parse_imagem(ref)
