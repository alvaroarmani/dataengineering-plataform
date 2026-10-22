"""Exercício 01 (M8) — Upsert idempotente no Postgres REAL. `pytest -q` (na bancada).

Roda a solução do aluno DUAS vezes e confere que o resultado é o mesmo (idempotência)
e que não há duplicatas.
"""
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

DDL = """
CREATE TABLE clientes (id INT PRIMARY KEY, nome TEXT);
INSERT INTO clientes (id, nome) VALUES (1, 'ana'), (2, 'bruno');
CREATE TABLE batch (id INT, nome TEXT);
INSERT INTO batch (id, nome) VALUES (2, 'bruno silva'), (3, 'caio');
"""


def _prep(pg):
    cur = pg.cursor()
    cur.execute(DDL)
    return cur


def _sql():
    return (RAIZ / "solucao.sql").read_text(encoding="utf-8")


def test_upsert_correto_e_idempotente(pg):
    cur = _prep(pg)
    cur.execute(_sql())  # 1a execução
    cur.execute(_sql())  # 2a execução — não pode duplicar nem mudar o resultado
    cur.execute("SELECT id, nome FROM clientes ORDER BY id")
    assert cur.fetchall() == [(1, "ana"), (2, "bruno silva"), (3, "caio")]


def test_sem_duplicatas(pg):
    cur = _prep(pg)
    cur.execute(_sql())
    cur.execute(_sql())
    cur.execute("SELECT COUNT(*), COUNT(DISTINCT id) FROM clientes")
    total, distintos = cur.fetchone()
    assert total == distintos == 3


def test_nova_carga_com_mudancas_e_refletida(pg):
    cur = _prep(pg)
    cur.execute(_sql())
    cur.execute("DELETE FROM batch; INSERT INTO batch (id, nome) VALUES (3, 'caio souza'), (4, 'duda')")
    cur.execute(_sql())                                   # carga do dia seguinte
    cur.execute("SELECT id, nome FROM clientes ORDER BY id")
    assert cur.fetchall() == [(1, "ana"), (2, "bruno silva"), (3, "caio souza"), (4, "duda")]


def test_batch_vazio_nao_apaga_o_destino(pg):
    cur = _prep(pg)
    cur.execute(_sql())
    cur.execute("DELETE FROM batch")                      # dia sem novidades
    cur.execute(_sql())                                   # truncate-and-load apagaria tudo
    cur.execute("SELECT id, nome FROM clientes ORDER BY id")
    assert cur.fetchall() == [(1, "ana"), (2, "bruno silva"), (3, "caio")]
