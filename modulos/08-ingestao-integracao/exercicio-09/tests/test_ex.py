"""Testes do Exercicio 09 (M8). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import aplicar_cdc  # noqa: E402


def test_aplicar_cdc():
    assert aplicar_cdc(*({1: 'a', 2: 'b'}, [{'op': 'U', 'chave': 1, 'valor': 'a2'}, {'op': 'D', 'chave': 2}, {'op': 'I', 'chave': 3, 'valor': 'c'}])) == {1: 'a2', 3: 'c'}
    assert aplicar_cdc(*({}, [{'op': 'I', 'chave': 1, 'valor': 'x'}])) == {1: 'x'}
