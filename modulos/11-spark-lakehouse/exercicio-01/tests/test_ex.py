import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import simular  # noqa: E402


def test_so_transformacoes_nao_leem_nada():
    assert simular(["filter", "select", "withColumn"]) == {"acoes": 0, "leituras_da_fonte": 0}


def test_cada_acao_rele_a_fonte():
    assert simular(["filter", "count", "show", "write"]) == {"acoes": 3, "leituras_da_fonte": 3}


def test_cache_materializa_na_primeira_acao():
    assert simular(["filter", "cache", "count", "show", "withColumn", "write"]) == {"acoes": 3, "leituras_da_fonte": 1}


def test_cache_depois_das_acoes_so_ajuda_as_seguintes():
    assert simular(["filter", "count", "cache", "show", "write"]) == {"acoes": 3, "leituras_da_fonte": 2}


def test_unpersist_volta_a_ler():
    assert simular(["cache", "count", "unpersist", "show"]) == {"acoes": 2, "leituras_da_fonte": 2}


def test_operacao_desconhecida():
    with pytest.raises(ValueError):
        simular(["filter", "explode_tudo"])
