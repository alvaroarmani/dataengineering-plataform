"""Testes do Exercício 05 (M12). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import esta_fresco  # noqa: E402


def test_esta_fresco():
    assert esta_fresco(*('2026-08-29 10:00', '2026-08-29 12:00', 6)) == True
    assert esta_fresco(*('2026-08-29 10:00', '2026-08-30 10:00', 6)) == False
