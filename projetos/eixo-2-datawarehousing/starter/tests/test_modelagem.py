"""Testes do Projeto Integrador do Eixo 2. Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from modelagem import construir_dim_produto, construir_fct_vendas, aplicar_scd2  # noqa: E402


def _csv(nome):
    return pd.read_csv(RAIZ / "data" / nome)


def test_dim_produto_surrogate_key():
    dim = construir_dim_produto(_csv("raw_produtos.csv"))
    assert list(dim.columns) == ["produto_sk", "produto_id", "nome", "categoria"]
    assert dim.to_dict("records") == [
        {"produto_sk": 1, "produto_id": 1, "nome": "Camiseta", "categoria": "roupas"},
        {"produto_sk": 2, "produto_id": 2, "nome": "Caneca", "categoria": "casa"},
        {"produto_sk": 3, "produto_id": 3, "nome": "Bone", "categoria": "roupas"},
    ]


def test_fct_vendas_fk_e_receita():
    dim = construir_dim_produto(_csv("raw_produtos.csv"))
    fct = construir_fct_vendas(_csv("raw_pedidos.csv"), dim)
    assert list(fct.columns) == ["pedido_id", "produto_sk", "cliente_id", "quantidade", "receita"]
    assert fct.to_dict("records") == [
        {"pedido_id": 1, "produto_sk": 1, "cliente_id": 1, "quantidade": 2, "receita": 99.8},
        {"pedido_id": 2, "produto_sk": 2, "cliente_id": 2, "quantidade": 1, "receita": 29.9},
        {"pedido_id": 3, "produto_sk": 3, "cliente_id": 1, "quantidade": 1, "receita": 39.9},
    ]


def test_fct_grao_unico():
    dim = construir_dim_produto(_csv("raw_produtos.csv"))
    fct = construir_fct_vendas(_csv("raw_pedidos.csv"), dim)
    assert fct["pedido_id"].is_unique  # grão: 1 linha por pedido


def test_scd2_historico():
    scd = aplicar_scd2(_csv("raw_produtos_historico.csv"))
    assert scd.to_dict("records") == [
        {"produto_id": 1, "categoria": "roupas", "valido_de": "2026-01-01", "valido_ate": "2026-06-01", "is_current": False},
        {"produto_id": 1, "categoria": "vestuario", "valido_de": "2026-06-01", "valido_ate": "9999-12-31", "is_current": True},
        {"produto_id": 2, "categoria": "casa", "valido_de": "2026-01-01", "valido_ate": "9999-12-31", "is_current": True},
    ]
