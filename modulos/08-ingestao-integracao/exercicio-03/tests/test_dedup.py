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


def _sql():
    return (RAIZ / "solucao.sql").read_text(encoding="utf-8")


def test_dedup_mais_recente(pg):
    cur = pg.cursor()
    cur.execute(DDL)
    cur.execute(_sql())
    assert cur.fetchall() == [(1, 150), (2, 200), (3, 300)]


def test_chegada_fora_de_ordem(pg):
    cur = pg.cursor()
    cur.execute(DDL)
    cur.execute("""INSERT INTO raw_eventos (id, valor, carregado_em) VALUES
      (2, 999, '2026-08-01'),   -- reentrega ANTIGA chegando depois: não pode vencer
      (3, 310, '2026-08-15'),   -- correção nova
      (4, 40,  '2026-08-12')""")
    cur.execute(_sql())
    assert cur.fetchall() == [(1, 150), (2, 200), (3, 310), (4, 40)]


def test_uma_linha_por_id(pg):
    cur = pg.cursor()
    cur.execute(DDL)
    cur.execute("INSERT INTO raw_eventos SELECT id, valor + 1, carregado_em - 30 FROM raw_eventos")
    cur.execute(_sql())
    linhas = cur.fetchall()
    assert [r[0] for r in linhas] == [1, 2, 3]                  # uma linha por id
    assert linhas == [(1, 150), (2, 200), (3, 300)]           # e é a versão nova, não a cópia antiga
