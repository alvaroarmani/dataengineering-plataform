import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import relatorio, status_freshness  # noqa: E402


@pytest.mark.parametrize("ultima, esperado", [
    ("2026-09-30 06:00", "ok"),        # 4 h de atraso
    ("2026-09-30 05:12", "ok"),        # atraso de exatamente 80% de 6 h (4 h 48): ainda ok
    ("2026-09-30 04:30", "aviso"),     # 5,5 h
    ("2026-09-30 04:00", "aviso"),     # exatamente 6 h: no limite, ainda não violou
    ("2026-09-30 03:59", "violado"),
    ("2026-09-29T10:00", "violado"),   # formato com T
])
def test_status(ultima, esperado):
    assert status_freshness(ultima, "2026-09-30 10:00", 6) == esperado


def test_aviso_configuravel():
    assert status_freshness("2026-09-30 07:00", "2026-09-30 10:00", 6, aviso_pct=0.5) == "ok"
    assert status_freshness("2026-09-30 06:59", "2026-09-30 10:00", 6, aviso_pct=0.5) == "aviso"


def test_ultima_no_futuro():
    with pytest.raises(ValueError):
        status_freshness("2026-09-30 11:00", "2026-09-30 10:00", 6)


def test_relatorio():
    tabelas = {"pedidos": "2026-09-30 09:00", "clientes": "2026-09-29 20:00", "estoque": "2026-09-30 05:00"}
    assert relatorio(tabelas, "2026-09-30 10:00", 6) == {
        "status": {"pedidos": "ok", "clientes": "violado", "estoque": "aviso"}, "pior": "clientes"}


def test_relatorio_empate_e_vazio():
    assert relatorio({"b": "2026-09-30 01:00", "a": "2026-09-30 01:00"}, "2026-09-30 02:00", 6)["pior"] == "a"
    with pytest.raises(ValueError):
        relatorio({}, "2026-09-30 02:00", 6)
