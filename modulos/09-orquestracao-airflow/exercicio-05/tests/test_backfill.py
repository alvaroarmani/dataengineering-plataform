"""Exercício 05 (M9) — Carga idempotente de um dia no Postgres REAL. `pytest -q` (na bancada).

Roda a solução DUAS vezes (simulando retry/backfill) e confere que o resultado é o mesmo,
sem duplicar, e sem tocar em outros dias.
"""
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

DDL = """
CREATE TABLE fato (data DATE, id INT, valor INT);
INSERT INTO fato (data, id, valor) VALUES ('2026-08-09', 1, 10);
CREATE TABLE batch (id INT, valor INT);
INSERT INTO batch (id, valor) VALUES (2, 20), (3, 30);
"""


def _rodar(pg):
    cur = pg.cursor()
    cur.execute((RAIZ / "solucao.sql").read_text(encoding="utf-8"))
    return cur


def test_idempotente_e_preserva_outros_dias(pg):
    cur = pg.cursor()
    cur.execute(DDL)
    _rodar(pg)  # 1a execução
    _rodar(pg)  # 2a execução (retry/backfill) — não pode duplicar
    cur.execute("SELECT to_char(data,'YYYY-MM-DD'), id, valor FROM fato ORDER BY data, id")
    assert cur.fetchall() == [
        ("2026-08-09", 1, 10),
        ("2026-08-10", 2, 20),
        ("2026-08-10", 3, 30),
    ]


def test_sem_duplicatas_no_dia(pg):
    cur = pg.cursor()
    cur.execute(DDL)
    _rodar(pg)
    _rodar(pg)
    cur.execute("SELECT COUNT(*) FROM fato WHERE data = DATE '2026-08-10'")
    assert cur.fetchone()[0] == 2
