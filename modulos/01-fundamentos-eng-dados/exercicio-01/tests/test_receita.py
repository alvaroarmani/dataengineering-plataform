"""Testes do Exercício 01. Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import receita_por_estado  # noqa: E402


def test_soma_por_estado():
    vendas = [
        {"estado": "SP", "valor": 100.0},
        {"estado": "SP", "valor": 50.0},
        {"estado": "RJ", "valor": 30.0},
    ]
    assert receita_por_estado(vendas) == {"SP": 150.0, "RJ": 30.0}


def test_ignora_valor_none():
    vendas = [
        {"estado": "SP", "valor": None},
        {"estado": "SP", "valor": 20.0},
    ]
    assert receita_por_estado(vendas) == {"SP": 20.0}


def test_lista_vazia():
    assert receita_por_estado([]) == {}


def test_um_estado_varias_vendas():
    vendas = [{"estado": "MG", "valor": 10.0} for _ in range(5)]
    assert receita_por_estado(vendas) == {"MG": 50.0}
