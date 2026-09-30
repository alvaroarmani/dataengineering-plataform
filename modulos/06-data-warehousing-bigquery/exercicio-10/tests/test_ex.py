import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import layout_recomendado  # noqa: E402

TIPOS = {"data_venda": "date", "loja_id": "int", "cliente_id": "string", "categoria": "string",
         "canal": "string", "uf": "string"}


def test_workload_de_painel():
    consultas = [(["data_venda", "loja_id"], 500), (["data_venda", "categoria"], 300),
                 (["cliente_id"], 800), (["uf", "canal"], 20), (["data_venda"], 50)]
    assert layout_recomendado(consultas, TIPOS) == {
        "particao": "data_venda", "cluster": ["cliente_id", "loja_id", "categoria", "canal"]}


def test_coluna_mais_filtrada_nem_sempre_particiona():
    # cliente_id é a mais filtrada, mas é string: não pode ser partição no BigQuery
    r = layout_recomendado([(["cliente_id"], 1000), (["loja_id"], 10)], TIPOS)
    assert r == {"particao": "loja_id", "cluster": ["cliente_id"]}


def test_sem_coluna_particionavel():
    assert layout_recomendado([(["uf"], 5), (["canal"], 5)], TIPOS) == {"particao": None, "cluster": ["canal", "uf"]}


def test_frequencia_pesa_mais_que_quantidade_de_consultas():
    consultas = [(["categoria"], 1)] * 10 + [(["canal"], 100)]
    assert layout_recomendado(consultas, TIPOS)["cluster"] == ["canal", "categoria"]


def test_coluna_sem_tipo():
    with pytest.raises(ValueError):
        layout_recomendado([(["xpto"], 1)], TIPOS)
