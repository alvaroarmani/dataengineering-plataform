"""Testes do Exercicio 10 (M6). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import layout_recomendado  # noqa: E402


def test_layout_recomendado():
    assert layout_recomendado(*([['data', 'cliente'], ['data'], ['data', 'produto'], ['cliente']],)) == {'particao': 'data', 'cluster': 'cliente'}
    assert layout_recomendado(*([['x']],)) == {'particao': 'x', 'cluster': None}
