import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import depende_de, propor_star  # noqa: E402

VENDAS = [
    {"pedido": 1, "cliente_id": 10, "cliente_nome": "Ana", "cidade": "Recife", "produto_id": "P1",
     "produto_nome": "Livro", "categoria": "livros", "qtd": 2, "valor": 80.0},
    {"pedido": 1, "cliente_id": 10, "cliente_nome": "Ana", "cidade": "Recife", "produto_id": "P2",
     "produto_nome": "Caneca", "categoria": "casa", "qtd": 1, "valor": 25.0},
    {"pedido": 2, "cliente_id": 11, "cliente_nome": "Bia", "cidade": "Natal", "produto_id": "P1",
     "produto_nome": "Livro", "categoria": "livros", "qtd": 1, "valor": 40.0},
    {"pedido": 3, "cliente_id": 10, "cliente_nome": "Ana", "cidade": "Recife", "produto_id": "P1",
     "produto_nome": "Livro", "categoria": "livros", "qtd": 1, "valor": 38.0},
]


def test_dependencias_funcionais():
    assert depende_de(VENDAS, "cliente_id") == ["cidade", "cliente_nome"]
    assert depende_de(VENDAS, "produto_id") == ["categoria", "produto_nome"]


def test_valor_nao_depende_do_produto():
    assert "valor" not in depende_de(VENDAS, "produto_id")      # P1 foi vendido por 80, 40 e 38


def test_star_proposto():
    assert propor_star(VENDAS, ["cliente_id", "produto_id"]) == {
        "fato": ["cliente_id", "produto_id", "pedido", "qtd", "valor"],
        "dim_cliente": ["cliente_id", "cidade", "cliente_nome"],
        "dim_produto": ["produto_id", "categoria", "produto_nome"],
    }


def test_dependencia_que_quebra_com_um_dado_novo():
    muda = VENDAS + [{**VENDAS[0], "pedido": 4, "cidade": "Olinda"}]    # a Ana se mudou
    assert depende_de(muda, "cliente_id") == ["cliente_nome"]
