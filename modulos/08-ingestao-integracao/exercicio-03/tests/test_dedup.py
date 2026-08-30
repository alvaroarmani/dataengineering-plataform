"""Exercício 03 (M8) — Dedup no Postgres REAL. `pytest -q` (na bancada)."""
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

DDL = """
CREATE TABLE raw_eventos (id INT, valor INT, carregado_em DATE);
INSERT INTO raw_eventos (id, valor, carregado_em) VALUES
  (1, 100, '2026-08-10'),
  (2, 200, '2026-08-10'),
  (3, 300, '2026-08-11'),
  (1, 150, '2026-08-12');
"""


def test_dedup_mais_recente(pg):
    cur = pg.cursor()
    cur.execute(DDL)
    cur.execute((RAIZ / "solucao.sql").read_text(encoding="utf-8"))
    assert cur.fetchall() == [(1, 150), (2, 200), (3, 300)]
