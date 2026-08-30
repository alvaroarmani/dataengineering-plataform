"""Testes do Exercício 06 (M10). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import parse_imagem  # noqa: E402


def test_parse_imagem():
    assert parse_imagem(*('postgres:16',)) == ('docker.io', 'postgres', '16')
    assert parse_imagem(*('postgres',)) == ('docker.io', 'postgres', 'latest')
    assert parse_imagem(*('ghcr.io/dbt-labs/dbt-postgres:1.8.2',)) == ('ghcr.io', 'dbt-labs/dbt-postgres', '1.8.2')
