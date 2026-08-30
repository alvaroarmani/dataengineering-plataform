"""Testes do Exercício 04 (M10). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import porta_host  # noqa: E402


def test_porta_host():
    assert porta_host(*(['8080:80', '5432:5432'], 80)) == 8080
    assert porta_host(*(['8080:80'], 9999)) == None
