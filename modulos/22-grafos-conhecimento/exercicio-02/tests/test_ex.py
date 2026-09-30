import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import fontes_e_sumidouros, graus  # noqa: E402

LINEAGE = {
    "raw_pedidos": ["stg_pedidos"],
    "raw_clientes": ["stg_clientes"],
    "stg_pedidos": ["fct_vendas", "fct_frete", "fct_vendas"],   # repetido de propósito
    "stg_clientes": ["dim_cliente", "fct_vendas"],
    "fct_vendas": ["dash_diretoria"],
    "dim_cliente": ["dash_diretoria"],
    "tabela_orfa": [],
}


def test_graus():
    assert graus(LINEAGE) == {
        "dash_diretoria": (2, 0), "dim_cliente": (1, 1), "fct_frete": (1, 0), "fct_vendas": (2, 1),
        "raw_clientes": (0, 1), "raw_pedidos": (0, 1), "stg_clientes": (1, 2), "stg_pedidos": (1, 2),
        "tabela_orfa": (0, 0)}


def test_fontes_e_sumidouros():
    assert fontes_e_sumidouros(LINEAGE) == {
        "fontes": ["raw_clientes", "raw_pedidos", "tabela_orfa"],
        "sumidouros": ["dash_diretoria", "fct_frete", "tabela_orfa"],
        "mais_dependida": "stg_clientes"}


def test_no_so_como_destino_existe():
    assert graus({"a": ["b"]}) == {"a": (0, 1), "b": (1, 0)}


def test_vazio():
    assert graus({}) == {}
    with pytest.raises(ValueError):
        fontes_e_sumidouros({})
