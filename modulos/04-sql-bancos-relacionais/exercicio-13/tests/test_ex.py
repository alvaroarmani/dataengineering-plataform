"""Testes do Exercicio 13 (M4). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import indice_recomendado  # noqa: E402


def test_indice_recomendado():
    assert indice_recomendado(*('igualdade',)) == 'hash'
    assert indice_recomendado(*('texto_busca',)) == 'gin'
    assert indice_recomendado(*('append_only',)) == 'brin'
    assert indice_recomendado(*('ordenacao',)) == 'btree'
