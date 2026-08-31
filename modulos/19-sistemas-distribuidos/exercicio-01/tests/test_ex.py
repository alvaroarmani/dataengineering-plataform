"""Testes do Exercício 01 (M19). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import custo_replicacao  # noqa: E402


def test_custo_replicacao():
    assert custo_replicacao(*(100, 3)) == 300
    assert custo_replicacao(*(50, 1)) == 50
