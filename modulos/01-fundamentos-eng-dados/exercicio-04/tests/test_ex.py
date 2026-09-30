"""Testes do Exercício 04 (M1). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import recomendar_arquitetura  # noqa: E402


def test_bi_sobre_dados_tabulares_e_warehouse():
    r = recomendar_arquitetura({"formatos": ["tabular"], "consumidores": ["bi"]})
    assert r == {"arquitetura": "data-warehouse", "motivos": ["bi_com_esquema"]}


def test_ml_sobre_logs_e_imagens_e_lake():
    r = recomendar_arquitetura({"formatos": ["log", "imagem"], "consumidores": ["ml"]})
    assert r == {"arquitetura": "data-lake", "motivos": ["consumo_ml", "dados_nao_estruturados"]}


def test_bi_e_ml_no_mesmo_dado_e_lakehouse():
    r = recomendar_arquitetura({"formatos": ["tabular", "json"], "consumidores": ["bi", "ml"]})
    assert r["arquitetura"] == "lakehouse"
    assert r["motivos"] == ["bi_com_esquema", "consumo_ml", "dados_nao_estruturados"]


def test_acid_sobre_lake_vira_lakehouse():
    # arquivar barato + precisar de ACID (ex.: correções/merge) = o caso que motivou o lakehouse
    r = recomendar_arquitetura({"formatos": ["tabular"], "consumidores": ["arquivamento"],
                                "precisa_acid": True})
    assert r == {"arquitetura": "lakehouse", "motivos": ["arquivamento_barato", "transacoes_acid"]}


def test_formato_tabular_sozinho_nao_pede_lake():
    r = recomendar_arquitetura({"formatos": ["tabular"], "consumidores": ["sql_adhoc"], "precisa_acid": True})
    assert r == {"arquitetura": "data-warehouse", "motivos": ["bi_com_esquema", "transacoes_acid"]}


def test_nao_muta_a_entrada():
    req = {"formatos": ["json"], "consumidores": ["ml", "bi"]}
    recomendar_arquitetura(req)
    assert req == {"formatos": ["json"], "consumidores": ["ml", "bi"]}


@pytest.mark.parametrize("req", [
    {"formatos": [], "consumidores": ["bi"]},
    {"formatos": ["tabular"], "consumidores": []},
    {"consumidores": ["bi"]},
    {"formatos": ["xml"], "consumidores": ["bi"]},
    {"formatos": ["tabular"], "consumidores": ["dashboard"]},
])
def test_requisito_invalido(req):
    with pytest.raises(ValueError):
        recomendar_arquitetura(req)
