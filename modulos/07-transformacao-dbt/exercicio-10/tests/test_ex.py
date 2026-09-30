import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import selecionar_incremental, simular_cargas  # noqa: E402

LINHAS = [{"id": 1, "updated_at": 3}, {"id": 2, "updated_at": 7}, {"id": 3, "updated_at": 5}]


def test_selecao_basica():
    assert selecionar_incremental(LINHAS, 4) == ([{"id": 2, "updated_at": 7}, {"id": 3, "updated_at": 5}], 7)
    assert selecionar_incremental(LINHAS, 10) == ([], 10)
    assert selecionar_incremental(LINHAS, None) == (LINHAS, 7)
    assert selecionar_incremental([], None) == ([], None)


def test_lookback_reabre_a_janela():
    sel, wm = selecionar_incremental(LINHAS, 7, lookback=3)
    assert [r["id"] for r in sel] == [2, 3] and wm == 7


# carga 1 vê o id 10 com updated_at=100; o id 11, com o MESMO updated_at, só chega depois;
# o id 12 chega atrasado com updated_at antigo
CHEGADAS = [[{"id": 10, "updated_at": 100}],
            [{"id": 11, "updated_at": 100}, {"id": 12, "updated_at": 98}],
            [{"id": 13, "updated_at": 105}]]


def test_sem_lookback_perde_linhas():
    assert simular_cargas(CHEGADAS, lookback=0) == {10, 13}


def test_com_lookback_nada_se_perde():
    assert simular_cargas(CHEGADAS, lookback=5) == {10, 11, 12, 13}


def test_lookback_invalido():
    with pytest.raises(ValueError):
        selecionar_incremental(LINHAS, 5, lookback=-1)
