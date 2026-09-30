import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import checar_unicidade  # noqa: E402

ITENS = [
    {"pedido": 10, "item": 1, "sku": "A"},
    {"pedido": 10, "item": 2, "sku": "B"},
    {"pedido": 10, "item": 1, "sku": "A"},     # reentrega
    {"pedido": 11, "item": 1, "sku": "C"},
    {"pedido": 12, "item": 1, "sku": "D"},
    {"pedido": 12, "item": 1, "sku": "D"},
    {"pedido": 12, "item": 1, "sku": "D"},
    {"pedido": None, "item": 1, "sku": "E"},
    {"pedido": 13, "sku": "F"},                # item ausente
]


def test_chave_composta():
    assert checar_unicidade(ITENS, ["pedido", "item"]) == {
        "duplicadas": [((12, 1), 3), ((10, 1), 2)], "chave_incompleta": 2}


def test_mesma_base_chave_simples_muda_a_resposta():
    r = checar_unicidade(ITENS, ["pedido"])
    assert r["duplicadas"] == [((10,), 3), ((12,), 3)]      # empate em 3: ordena pela chave
    assert r["chave_incompleta"] == 1


def test_sem_duplicatas():
    assert checar_unicidade(ITENS[:2], ["pedido", "item"]) == {"duplicadas": [], "chave_incompleta": 0}


def test_nulos_nao_viram_duplicata_entre_si():
    linhas = [{"k": None}, {"k": None}, {"k": None}]
    assert checar_unicidade(linhas, ["k"]) == {"duplicadas": [], "chave_incompleta": 3}


def test_chave_vazia():
    with pytest.raises(ValueError):
        checar_unicidade(ITENS, [])
