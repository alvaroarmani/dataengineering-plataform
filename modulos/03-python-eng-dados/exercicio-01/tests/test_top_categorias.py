"""Testes do Exercício 01 (M3). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import top_n_categorias  # noqa: E402


# receita: eletronicos=2000; casa=80; livros=80 (empate casa/livros -> alfabético)
PEDIDOS = [
    {"categoria": "livros", "valor": 50},
    {"categoria": "eletronicos", "valor": 1200},
    {"categoria": "livros", "valor": 30},
    {"categoria": "casa", "valor": 80},
    {"categoria": "eletronicos", "valor": 800},
]


def test_top_1():
    assert top_n_categorias(PEDIDOS, 1) == [("eletronicos", 2000.0)]


def test_top_2_com_empate_alfabetico():
    # 2º e 3º empatam em 80 -> 'casa' vem antes de 'livros'
    assert top_n_categorias(PEDIDOS, 2) == [("eletronicos", 2000.0), ("casa", 80.0)]


def test_ordem_completa():
    assert top_n_categorias(PEDIDOS, 10) == [
        ("eletronicos", 2000.0),
        ("casa", 80.0),
        ("livros", 80.0),
    ]


def test_desempate_alfabetico_simples():
    dados = [{"categoria": "b", "valor": 10}, {"categoria": "a", "valor": 10}]
    assert top_n_categorias(dados, 2) == [("a", 10.0), ("b", 10.0)]


def test_lista_vazia():
    assert top_n_categorias([], 3) == []
