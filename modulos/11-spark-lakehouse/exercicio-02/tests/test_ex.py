"""Testes do Exercício 02 (M11). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import primeira_acao  # noqa: E402


def test_primeira_acao():
    assert primeira_acao(*(['filter', 'select', 'count', 'show'],)) == 2
    assert primeira_acao(*(['filter', 'select'],)) == -1
    assert primeira_acao(*(['collect'],)) == 0
