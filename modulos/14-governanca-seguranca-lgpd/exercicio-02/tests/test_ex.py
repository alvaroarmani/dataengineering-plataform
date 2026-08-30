"""Testes do Exercício 02 (M14). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import tabelas_sem_dono  # noqa: E402


def test_tabelas_sem_dono():
    assert tabelas_sem_dono(*({'a': 'ana', 'b': '', 'c': None, 'd': 'caio'},)) == ['b', 'c']
    assert tabelas_sem_dono(*({'x': 'ana'},)) == []
