import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import selecao_slim_ci  # noqa: E402

DAG = {
    "stg_pedidos": ["int_pedidos_itens"],
    "stg_itens": ["int_pedidos_itens"],
    "stg_clientes": ["dim_cliente"],
    "int_pedidos_itens": ["fct_vendas"],
    "dim_cliente": ["fct_vendas", "mart_clientes"],
    "fct_vendas": ["mart_receita"],
    "mart_receita": [],
    "mart_clientes": [],
}


def test_mudanca_na_base_propaga_ate_o_mart():
    assert selecao_slim_ci(["models/staging/stg_pedidos.sql"], DAG) == [
        "fct_vendas", "int_pedidos_itens", "mart_receita", "stg_pedidos"]


def test_duas_mudancas_uniao_sem_repetir():
    assert selecao_slim_ci(["models/staging/stg_clientes.sql", "models/marts/fct_vendas.sql"], DAG) == [
        "dim_cliente", "fct_vendas", "mart_clientes", "mart_receita", "stg_clientes"]


def test_folha_so_ela():
    assert selecao_slim_ci(["models/marts/mart_receita.sql"], DAG) == ["mart_receita"]


def test_so_documentacao_nao_roda_nada():
    assert selecao_slim_ci(["README.md", "models/marts/schema.yml", "docs/overview.md"], DAG) == []


def test_macro_ou_projeto_rodam_tudo():
    assert selecao_slim_ci(["macros/cents_to_reais.sql"], DAG) == sorted(DAG)
    assert selecao_slim_ci(["dbt_project.yml"], DAG) == sorted(DAG)


def test_modelo_desconhecido():
    with pytest.raises(ValueError):
        selecao_slim_ci(["models/staging/stg_fantasma.sql"], DAG)
