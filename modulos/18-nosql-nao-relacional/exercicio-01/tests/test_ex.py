"""Testes do Exercício 01 (M18). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import familia_nosql  # noqa: E402


def test_familia_nosql():
    assert familia_nosql(*('cache',)) == 'key-value'
    assert familia_nosql(*('catalogo',)) == 'documento'
    assert familia_nosql(*('metricas',)) == 'time-series'
    assert familia_nosql(*('transacao',)) == 'relacional'
