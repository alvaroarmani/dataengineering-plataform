import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import analisar_plano  # noqa: E402

PLANO = [("filter",), ("join", 50), ("withColumn",), ("groupBy",), ("join", 2), ("orderBy",), ("coalesce",)]


def test_plano_tipico():
    assert analisar_plano(PLANO) == {"stages": 4, "shuffles": 3, "broadcasts": 1}


def test_subir_o_limite_tira_um_shuffle():
    assert analisar_plano(PLANO, limite_broadcast_mb=64) == {"stages": 3, "shuffles": 2, "broadcasts": 2}


def test_so_narrow_e_um_stage():
    assert analisar_plano([("filter",), ("select",), ("withColumn",), ("coalesce",)]) == {
        "stages": 1, "shuffles": 0, "broadcasts": 0}


def test_repartition_e_distinct_embaralham():
    assert analisar_plano([("repartition",), ("distinct",)])["shuffles"] == 2


def test_passo_desconhecido():
    with pytest.raises(ValueError):
        analisar_plano([("explode_tudo",)])
