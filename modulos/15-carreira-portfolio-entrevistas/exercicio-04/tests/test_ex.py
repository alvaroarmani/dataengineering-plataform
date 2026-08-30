"""Testes do Exercício 04 (M15). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import separar_fato_dim  # noqa: E402


def test_separar_fato_dim():
    assert separar_fato_dim(*([('valor', 'medida'), ('categoria', 'descritivo'), ('quantidade', 'medida'), ('cidade', 'descritivo')],)) == {'fato': ['quantidade', 'valor'], 'dimensao': ['categoria', 'cidade']}
    assert separar_fato_dim(*([('nome', 'descritivo')],)) == {'fato': [], 'dimensao': ['nome']}
