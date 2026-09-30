import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import backfill, carregar_dia  # noqa: E402

FATO = [("2026-08-09", 1, 10), ("2026-08-10", 9, 99), ("2026-08-11", 5, 50), ("2026-08-12", 7, 70)]


def test_overwrite_de_um_dia():
    assert carregar_dia(FATO, "2026-08-10", [(2, 20), (3, 30)]) == [
        ("2026-08-09", 1, 10), ("2026-08-10", 2, 20), ("2026-08-10", 3, 30),
        ("2026-08-11", 5, 50), ("2026-08-12", 7, 70)]


def test_lote_duplicado():
    with pytest.raises(ValueError):
        carregar_dia(FATO, "2026-08-10", [(2, 20), (2, 21)])


FONTE_CORRIGIDA = {"2026-08-10": [(2, 20), (3, 30)], "2026-08-11": [(5, 55)]}


def test_backfill_substitui_e_esvazia():
    r = backfill(FATO, FONTE_CORRIGIDA, "2026-08-10", "2026-08-12")
    assert r == [("2026-08-09", 1, 10), ("2026-08-10", 2, 20), ("2026-08-10", 3, 30), ("2026-08-11", 5, 55)]


def test_backfill_e_idempotente_e_catchup_sobreposto():
    uma = backfill(FATO, FONTE_CORRIGIDA, "2026-08-10", "2026-08-12")
    assert backfill(uma, FONTE_CORRIGIDA, "2026-08-10", "2026-08-12") == uma
    assert backfill(backfill(FATO, FONTE_CORRIGIDA, "2026-08-10", "2026-08-11"),
                    FONTE_CORRIGIDA, "2026-08-11", "2026-08-12") == uma


def test_intervalo_invalido():
    with pytest.raises(ValueError):
        backfill(FATO, {}, "2026-08-12", "2026-08-10")
