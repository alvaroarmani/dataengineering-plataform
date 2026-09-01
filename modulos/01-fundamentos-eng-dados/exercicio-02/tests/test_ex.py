"""Testes do Exercicio 02 (M1). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import classifica_carga  # noqa: E402


def test_classifica_carga():
    assert classifica_carga(*('transacao',)) == 'OLTP'
    assert classifica_carga(*('agregacao',)) == 'OLAP'
    assert classifica_carga(*('historico',)) == 'OLAP'
    assert classifica_carga(*('outro',)) == 'indefinido'
