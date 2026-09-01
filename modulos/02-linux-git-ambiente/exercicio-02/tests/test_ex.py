"""Testes do Exercicio 02 (M2). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import deve_versionar  # noqa: E402


def test_deve_versionar():
    assert deve_versionar(*('.env',)) == False
    assert deve_versionar(*('main.py',)) == True
    assert deve_versionar(*('app.pyc',)) == False
    assert deve_versionar(*('README.md',)) == True
