"""Testes do Exercício 01 (M21). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import custo_consulta  # noqa: E402


def test_custo_consulta():
    assert custo_consulta(*(2, 5.0)) == 10.0
    assert custo_consulta(*(0.5, 5.0)) == 2.5
