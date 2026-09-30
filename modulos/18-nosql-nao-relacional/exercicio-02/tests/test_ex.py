import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import copy

from solucao import agregar  # noqa: E402

PEDIDOS = [
    {"_id": 1, "status": "pago", "cliente": {"cidade": "Recife"},
     "itens": [{"sku": "livro", "qtd": 2, "valor": 80.0}, {"sku": "caneca", "qtd": 1, "valor": 25.0}]},
    {"_id": 2, "status": "pago", "cliente": {"cidade": "Natal"},
     "itens": [{"sku": "livro", "qtd": 1, "valor": 40.0}]},
    {"_id": 3, "status": "cancelado", "cliente": {"cidade": "Recife"},
     "itens": [{"sku": "caneca", "qtd": 3, "valor": 75.0}]},
    {"_id": 4, "status": "pago", "cliente": {"cidade": "Recife"}, "itens": []},
]


def test_match_aninhado_e_group_count():
    r = agregar(PEDIDOS, [{"$match": {"status": "pago"}},
                          {"$group": {"_id": "$cliente.cidade", "pedidos": {"$sum": 1}}}])
    assert r == [{"_id": "Recife", "pedidos": 2}, {"_id": "Natal", "pedidos": 1}]


def test_unwind_e_receita_por_sku():
    r = agregar(PEDIDOS, [{"$match": {"status": "pago"}},
                          {"$unwind": "itens"},
                          {"$group": {"_id": "$itens.sku", "receita": {"$sum": "$itens.valor"},
                                      "qtd": {"$sum": "$itens.qtd"}}},
                          {"$sort": {"receita": -1}}])
    assert r == [{"_id": "livro", "receita": 120.0, "qtd": 3}, {"_id": "caneca", "receita": 25.0, "qtd": 1}]


def test_unwind_de_array_vazio_some():
    assert [d["_id"] for d in agregar(PEDIDOS, [{"$unwind": "itens"}])] == [1, 1, 2, 3]


def test_avg_e_sort_com_duas_chaves():
    r = agregar(PEDIDOS, [{"$unwind": "itens"},
                          {"$group": {"_id": "$cliente.cidade", "ticket": {"$avg": "$itens.valor"}}},
                          {"$sort": {"ticket": -1, "_id": 1}}])
    assert r == [{"_id": "Recife", "ticket": 60.0}, {"_id": "Natal", "ticket": 40.0}]


def test_nao_altera_a_entrada_e_estagio_invalido():
    antes = copy.deepcopy(PEDIDOS)
    agregar(PEDIDOS, [{"$unwind": "itens"}])
    assert PEDIDOS == antes
    with pytest.raises(ValueError):
        agregar(PEDIDOS, [{"$lookup": {}}])
