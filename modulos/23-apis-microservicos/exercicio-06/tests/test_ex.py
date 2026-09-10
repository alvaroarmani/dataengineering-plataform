"""Testes do Exercicio 06 (M23). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import campos_faltando  # noqa: E402


def test_campos_faltando():
    assert campos_faltando(*({'nome': 'a'}, ['nome', 'email'])) == ['email']
    assert campos_faltando(*({'nome': 'a', 'email': 'b'}, ['nome', 'email'])) == []
