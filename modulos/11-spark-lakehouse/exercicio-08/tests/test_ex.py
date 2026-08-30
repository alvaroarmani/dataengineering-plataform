"""Testes do Exercício 08 (M11). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import aceita_escrita  # noqa: E402


def test_aceita_escrita():
    assert aceita_escrita(*({'id': 'int', 'nome': 'str'}, {'id': 1, 'nome': 'a'})) == True
    assert aceita_escrita(*({'id': 'int', 'nome': 'str'}, {'id': 'x', 'nome': 'a'})) == False
    assert aceita_escrita(*({'id': 'int'}, {})) == False
