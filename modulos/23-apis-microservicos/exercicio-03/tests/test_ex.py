"""Testes do Exercicio 03 (M23). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import deve_processar  # noqa: E402


def test_deve_processar():
    assert deve_processar(*(['a', 'b'], 'c')) == True
    assert deve_processar(*(['a', 'b'], 'a')) == False
