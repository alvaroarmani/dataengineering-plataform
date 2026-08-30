"""Testes do Exercício 03 (M10). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import ordem_subida  # noqa: E402


def test_ordem_subida():
    assert ordem_subida(*(['db', 'api', 'web'], [('db', 'api'), ('api', 'web')])) == ['db', 'api', 'web']
    assert ordem_subida(*(['db', 'cache', 'api'], [('db', 'api'), ('cache', 'api')])) == ['db', 'cache', 'api']
