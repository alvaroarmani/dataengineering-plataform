"""Testes do Exercicio 05 (M1). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import bytes_colunar  # noqa: E402


def test_bytes_colunar():
    assert bytes_colunar(*(100, 3, 10)) == 30
    assert bytes_colunar(*(50, 50, 2)) == 100
