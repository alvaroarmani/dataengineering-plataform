"""Exercício 03 (M6) — Particionamento no Postgres REAL. `pytest -q` (na bancada).

Cria uma tabela PARTICIONADA por ano (particionamento declarativo do Postgres), insere
dados de fixture, executa as queries do aluno (consulta_a.sql / consulta_b.sql) e confere.
A fixture `pg` faz rollback ao final (não suja o banco).
"""
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

DDL = """
CREATE TABLE pedidos(ano int, mes int, categoria text, valor int) PARTITION BY RANGE (ano);
CREATE TABLE pedidos_2023 PARTITION OF pedidos FOR VALUES FROM (2023) TO (2024);
CREATE TABLE pedidos_2024 PARTITION OF pedidos FOR VALUES FROM (2024) TO (2025);
CREATE TABLE pedidos_2025 PARTITION OF pedidos FOR VALUES FROM (2025) TO (2026);
INSERT INTO pedidos (ano, mes, categoria, valor) VALUES
  (2024,1,'A',100),(2024,2,'B',200),
  (2025,1,'A',300),(2025,1,'B',150),(2025,2,'A',250),(2025,3,'A',100),
  (2023,12,'B',50);
"""


def _sql(nome):
    return (RAIZ / nome).read_text(encoding="utf-8")


def _setup(pg):
    cur = pg.cursor()
    cur.execute(DDL)
    return cur


def test_receita_mensal_2025(pg):
    cur = _setup(pg)
    cur.execute(_sql("consulta_a.sql"))
    assert cur.fetchall() == [(1, 450), (2, 250), (3, 100)]


def test_total_por_ano_desde_2024(pg):
    cur = _setup(pg)
    cur.execute(_sql("consulta_b.sql"))
    assert cur.fetchall() == [(2024, 300), (2025, 800)]
