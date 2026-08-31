"""Testes do Exercício 05 (M17). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import janela_tumbling  # noqa: E402


def test_janela_tumbling():
    assert janela_tumbling(*(659, 60)) == 600
    assert janela_tumbling(*(600, 60)) == 600
    assert janela_tumbling(*(125, 60)) == 120
