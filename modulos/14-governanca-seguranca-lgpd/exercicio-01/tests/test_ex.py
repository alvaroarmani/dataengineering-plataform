import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import analise_de_impacto  # noqa: E402

LINEAGE = {
    "stg_pedidos": ["fct_vendas", "fct_frete"],
    "fct_vendas": ["mart_receita", "dash_comercial"],
    "fct_frete": ["dash_logistica"],
    "mart_receita": ["dash_diretoria", "reconciliacao"],
    "reconciliacao": ["mart_receita"],          # ciclo
    "dash_comercial": [], "dash_logistica": [], "dash_diretoria": [],
    "stg_clientes": ["dim_cliente"], "dim_cliente": [],
}
DONOS = {"fct_vendas": "ana", "fct_frete": "bruno", "mart_receita": "ana",
         "dash_comercial": "carla", "dash_diretoria": "diretoria-bi", "reconciliacao": None,
         "dash_logistica": ""}


def test_impacto_completo():
    r = analise_de_impacto(LINEAGE, "stg_pedidos", DONOS)
    assert r["impactados"] == ["dash_comercial", "dash_diretoria", "dash_logistica", "fct_frete",
                               "fct_vendas", "mart_receita", "reconciliacao"]
    assert r["por_distancia"] == {1: ["fct_frete", "fct_vendas"],
                                  2: ["dash_comercial", "dash_logistica", "mart_receita"],
                                  3: ["dash_diretoria", "reconciliacao"]}


def test_quem_notificar_e_quem_nao_tem_dono():
    r = analise_de_impacto(LINEAGE, "stg_pedidos", DONOS)
    assert r["notificar"] == ["ana", "bruno", "carla", "diretoria-bi"]
    assert r["sem_dono"] == ["dash_logistica", "reconciliacao"]


def test_ciclo_nao_trava_e_nao_se_inclui():
    r = analise_de_impacto(LINEAGE, "mart_receita", DONOS)
    assert r["impactados"] == ["dash_diretoria", "reconciliacao"]


def test_folha_e_desconhecido():
    assert analise_de_impacto(LINEAGE, "dim_cliente", DONOS) == {
        "impactados": [], "por_distancia": {}, "notificar": [], "sem_dono": []}
    with pytest.raises(KeyError):
        analise_de_impacto(LINEAGE, "stg_fantasma", DONOS)
