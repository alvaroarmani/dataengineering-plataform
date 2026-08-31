"""Testes do Exercício 03 (M17). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import particao  # noqa: E402


def test_particao():
    assert particao(*('cliente-42', 3)) == 2
    assert particao(*('cliente-7', 3)) == 0
    assert particao(*('cliente-42', 3)) == 2
