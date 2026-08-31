"""Testes do Exercício 02 (M19). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import no_no_anel  # noqa: E402


def test_no_no_anel():
    assert no_no_anel(*(25, [10, 20, 30, 40])) == 30
    assert no_no_anel(*(45, [10, 20, 30, 40])) == 10
    assert no_no_anel(*(10, [10, 20])) == 10
