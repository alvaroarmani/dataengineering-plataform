"""Testes do Exercício 02 (M3). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import Pipeline  # noqa: E402


def test_sem_passos_retorna_igual():
    assert Pipeline().rodar([1, 2, 3]) == [1, 2, 3]


def test_um_passo():
    p = Pipeline([lambda xs: [x * 2 for x in xs]])
    assert p.rodar([1, 2, 3]) == [2, 4, 6]


def test_ordem_dos_passos():
    p = Pipeline([
        lambda xs: [x for x in xs if x > 0],
        lambda xs: [x * 10 for x in xs],
    ])
    assert p.rodar([-1, 2, 3]) == [20, 30]


def test_adicionar_encadeado_retorna_self():
    p = Pipeline()
    r = p.adicionar(lambda xs: xs + [0])
    assert r is p  # adicionar retorna self
    p.adicionar(lambda xs: xs[::-1])
    assert p.rodar([1, 2]) == [0, 2, 1]


def test_default_nao_compartilhado():
    a = Pipeline()
    a.adicionar(lambda xs: xs)
    b = Pipeline()
    assert b.passos == []  # cada instância tem sua própria lista
