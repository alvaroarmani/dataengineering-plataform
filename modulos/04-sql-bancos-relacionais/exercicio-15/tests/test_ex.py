"""Testes do Exercício 15 (M4) — SQL em dados REAIS. Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

import duckdb
import pytest

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import CONSULTA_A, CONSULTA_B, CONSULTA_C, CONSULTA_D  # noqa: E402

AMOSTRAS = RAIZ / "datasets" / "amostras"


def _conectar(filtro=""):
    c = duckdb.connect()
    c.execute(f"CREATE TABLE corridas AS SELECT * FROM read_csv_auto("
              f"'{(AMOSTRAS / 'nyc_taxi_2024_01_amostra.csv').as_posix()}') {filtro}")
    c.execute(f"CREATE TABLE zonas AS SELECT * FROM read_csv_auto("
              f"'{(AMOSTRAS / 'taxi_zone_lookup.csv').as_posix()}')")
    return c


@pytest.fixture(scope="module")
def con():
    return _conectar()


@pytest.fixture(scope="module")
def con_v2():
    return _conectar("WHERE VendorID = 2")


# ---------- A) top zonas (JOIN + GROUP BY) ----------
def test_a_top_zonas(con):
    assert con.execute(CONSULTA_A).fetchall() == [
        ("Upper East Side South", "Manhattan", 131, 2624.72),
        ("Midtown Center", "Manhattan", 130, 3175.82),
        ("JFK Airport", "Queens", 127, 12089.25),
        ("Upper East Side North", "Manhattan", 103, 2193.78),
        ("Penn Station/Madison Sq West", "Manhattan", 100, 2139.06),
    ]


def test_a_outra_base(con_v2):
    assert [r[0] for r in con_v2.execute(CONSULTA_A).fetchall()] == [
        "Midtown Center", "JFK Airport", "Upper East Side South", "Penn Station/Madison Sq West", "Midtown East"]


# ---------- B) por hora (EXTRACT + HAVING) ----------
def test_b_ticket_por_hora(con):
    r = con.execute(CONSULTA_B).fetchall()
    assert len(r) == 15                                   # HAVING corta as horas com < 100 corridas
    assert r[:3] == [(21, 126, 36.74), (14, 167, 31.55), (19, 148, 30.92)]
    assert r[-1] == (12, 138, 24.96)
    assert all(n >= 100 for _, n, _ in r)


def test_b_outra_base(con_v2):
    r = con_v2.execute(CONSULTA_B).fetchall()
    assert len(r) == 8 and r[0] == (19, 115, 32.53) and r[-1] == (12, 101, 25.51)


# ---------- C) top-1 por grupo (window function) ----------
def test_c_zona_campea_por_borough(con):
    assert con.execute(CONSULTA_C).fetchall() == [
        ("Bronx", "Mott Haven/Port Morris", 2156.26),
        ("Brooklyn", "Boerum Hill", 145.53),
        ("Manhattan", "Midtown Center", 3175.82),     # a campeã de receita não é a campeã de volume
        ("Queens", "JFK Airport", 12089.25),
    ]


def test_c_outra_base(con_v2):
    assert con_v2.execute(CONSULTA_C).fetchall() == [
        ("Bronx", "Mott Haven/Port Morris", 2156.26),
        ("Brooklyn", "Boerum Hill", 145.53),
        ("Manhattan", "Midtown Center", 2437.89),
        ("Queens", "JFK Airport", 9473.67),
    ]


# ---------- D) diagnóstico (CASE + % com window sobre agregado) ----------
def test_d_diagnostico(con):
    r = con.execute(CONSULTA_D).fetchall()
    assert r == [
        ("ok", 2394, 91.48),
        ("passageiros_nulo", 150, 5.73),
        ("tarifa_nao_positiva", 53, 2.03),
        ("desembarque_antes", 20, 0.76),
    ]
    assert sum(n for _, n, _ in r) == con.execute("SELECT COUNT(*) FROM corridas").fetchone()[0]


def test_d_outra_base_e_pct_fecha_100(con_v2):
    r = con_v2.execute(CONSULTA_D).fetchall()
    assert r == [("ok", 1754, 92.36), ("passageiros_nulo", 92, 4.84), ("tarifa_nao_positiva", 53, 2.79)]
    assert sum(p for _, _, p in r) == pytest.approx(100, abs=0.02)
