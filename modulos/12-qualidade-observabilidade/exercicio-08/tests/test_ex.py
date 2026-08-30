"""Testes do Exercício 08 (M12). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import fora_da_faixa  # noqa: E402


def test_fora_da_faixa():
    assert fora_da_faixa(*(5, 0, 10)) == False
    assert fora_da_faixa(*(15, 0, 10)) == True
    assert fora_da_faixa(*(-1, 0, 10)) == True
