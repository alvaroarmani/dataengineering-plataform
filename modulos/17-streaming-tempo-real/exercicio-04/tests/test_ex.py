"""Testes do Exercício 04 (M17). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import lag_total  # noqa: E402


def test_lag_total():
    assert lag_total(*({0: 100, 1: 80, 2: 50}, {0: 100, 1: 60, 2: 50})) == 20
    assert lag_total(*({0: 10}, {0: 10})) == 0
    assert lag_total(*({0: 5, 1: 5}, {})) == 10
