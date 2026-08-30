"""Testes do Exercício 03 (M12). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import duplicados  # noqa: E402


def test_duplicados():
    assert duplicados(*([1, 2, 2, 3, 3, 3],)) == [2, 3]
    assert duplicados(*([1, 2, 3],)) == []
