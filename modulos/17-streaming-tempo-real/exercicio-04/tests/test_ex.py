import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import atribuir_range, lag_por_consumidor  # noqa: E402


def test_divisao_nao_exata():
    assert atribuir_range(7, ["c3", "c1", "c2"]) == {"c1": [0, 1, 2], "c2": [3, 4], "c3": [5, 6]}


def test_consumidores_demais_ficam_ociosos():
    assert atribuir_range(3, ["a", "b", "c", "d", "e"]) == {"a": [0], "b": [1], "c": [2], "d": [], "e": []}


def test_divisao_exata_e_grupo_vazio():
    assert atribuir_range(4, ["x", "y"]) == {"x": [0, 1], "y": [2, 3]}
    with pytest.raises(ValueError):
        atribuir_range(4, [])


def test_lag_por_consumidor():
    atrib = atribuir_range(6, ["a", "b", "c"])          # a: 0,1  b: 2,3  c: 4,5
    fim = {0: 100, 1: 100, 2: 500, 3: 480, 4: 90, 5: 95}
    commits = {0: 100, 1: 98, 2: 120, 3: 130, 4: 90}
    assert lag_por_consumidor(fim, commits, atrib) == {"a": 2, "b": 730, "c": 95, "_mais_atrasado": "b"}


def test_sem_lag_e_commit_invalido():
    atrib = {"a": [0], "b": []}
    assert lag_por_consumidor({0: 10}, {0: 10}, atrib) == {"a": 0, "b": 0, "_mais_atrasado": None}
    with pytest.raises(ValueError):
        lag_por_consumidor({0: 10}, {0: 11}, atrib)
