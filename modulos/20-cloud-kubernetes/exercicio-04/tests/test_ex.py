"""Testes do Exercício 04 (M20). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import hpa_replicas  # noqa: E402


def test_hpa_replicas():
    assert hpa_replicas(*(2, 90, 50)) == 4
    assert hpa_replicas(*(3, 50, 50)) == 3
    assert hpa_replicas(*(4, 10, 50)) == 1
