"""Testes do Exercício 01 (M18). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import atualizar_cidade, montar_documentos, pedidos_do_cliente  # noqa: E402

CLIENTES = [{"id": 1, "nome": "Ana", "cidade": "Recife"},
            {"id": 2, "nome": "Bruno", "cidade": "Curitiba"}]
PEDIDOS = [{"id": 12, "cliente_id": 1, "data": "2026-03-05"},
           {"id": 10, "cliente_id": 1, "data": "2026-03-01"},
           {"id": 11, "cliente_id": 2, "data": "2026-03-02"},
           {"id": 13, "cliente_id": 1, "data": "2026-03-09"}]
ITENS = [{"pedido_id": 10, "produto": "livro", "qtd": 2, "preco": 39.9},
         {"pedido_id": 11, "produto": "caneca", "qtd": 1, "preco": 25.0},
         {"pedido_id": 10, "produto": "marcador", "qtd": 3, "preco": 1.1},
         {"pedido_id": 12, "produto": "livro", "qtd": 1, "preco": 39.9}]


@pytest.fixture
def docs():
    return montar_documentos(CLIENTES, PEDIDOS, ITENS)


def test_um_documento_por_pedido_ordenado(docs):
    assert [d["_id"] for d in docs] == [10, 11, 12, 13]


def test_documento_completo(docs):
    assert docs[0] == {
        "_id": 10, "data": "2026-03-01",
        "cliente": {"id": 1, "nome": "Ana", "cidade": "Recife"},
        "itens": [{"produto": "livro", "qtd": 2, "preco": 39.9},
                  {"produto": "marcador", "qtd": 3, "preco": 1.1}],
        "total": 83.1,
    }


def test_pedido_sem_itens(docs):
    assert docs[3]["itens"] == [] and docs[3]["total"] == 0.0


def test_pedidos_do_cliente(docs):
    assert pedidos_do_cliente(docs, 1) == [10, 12, 13]
    assert pedidos_do_cliente(docs, 2) == [11]
    assert pedidos_do_cliente(docs, 99) == []


def test_mudanca_de_cidade_custa_uma_escrita_por_copia(docs):
    assert atualizar_cidade(docs, 1, "Olinda") == 3          # 3 pedidos da Ana = 3 escritas
    assert {d["cliente"]["cidade"] for d in docs if d["cliente"]["id"] == 1} == {"Olinda"}
    assert docs[1]["cliente"]["cidade"] == "Curitiba"         # o Bruno não foi tocado
    assert atualizar_cidade(docs, 1, "Olinda") == 0           # idempotente: nada mudou


def test_copias_sao_independentes(docs):
    docs[0]["cliente"]["nome"] = "ALTERADO"
    assert docs[2]["cliente"]["nome"] == "Ana"                # não é o mesmo objeto
    assert CLIENTES[0]["nome"] == "Ana"                        # e a entrada ficou intacta


def test_integridade_referencial():
    with pytest.raises(ValueError):
        montar_documentos(CLIENTES, [{"id": 20, "cliente_id": 99, "data": "2026-03-01"}], [])
    with pytest.raises(ValueError):
        montar_documentos(CLIENTES, PEDIDOS, ITENS + [{"pedido_id": 77, "produto": "x", "qtd": 1, "preco": 1.0}])
