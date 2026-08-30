"""Testes do Exercício 06 (M14). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import anonimizar  # noqa: E402


def test_anonimizar():
    assert anonimizar(*({'nome': 'ana', 'cpf': '123', 'valor': 10}, ['nome', 'cpf'])) == {'nome': '***', 'cpf': '***', 'valor': 10}
    assert anonimizar(*({'valor': 5}, ['nome'])) == {'valor': 5}
