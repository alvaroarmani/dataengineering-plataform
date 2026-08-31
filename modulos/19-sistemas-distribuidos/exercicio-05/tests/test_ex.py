"""Testes do Exercício 05 (M19). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import replica_atrasada  # noqa: E402


def test_replica_atrasada():
    assert replica_atrasada(*(100, 90, 5)) == True
    assert replica_atrasada(*(100, 98, 5)) == False
    assert replica_atrasada(*(100, 95, 5)) == False
