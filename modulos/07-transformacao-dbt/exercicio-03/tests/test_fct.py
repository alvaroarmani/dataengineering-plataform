"""Grader do Exercício 03 (M7) — confere o mart `fct_receita_categoria` (dbt).

Pré-requisito: `dbt build` na bancada (ver enunciado). Os testes de schema do dbt
(not_null/unique) cobrem integridade; aqui checamos os VALORES da agregação e a linhagem.
"""
import re
from pathlib import Path

import pytest

MODEL = Path(__file__).resolve().parents[1] / "projeto_dbt" / "models" / "fct_receita_categoria.sql"


def _consulta(pg, sql):
    cur = pg.cursor()
    cur.execute("SET search_path TO m7_ex03")              # o schema do profiles.yml deste exercício
    try:
        cur.execute(sql)
    except Exception as e:  # noqa: BLE001
        pg.rollback()
        if getattr(e, "pgcode", None) != "42P01":    # só "tabela não existe" é skip
            raise
        pytest.skip(f"fct_receita_categoria não encontrado ({e}). Rode `dbt build` primeiro.")
    return cur.fetchall()


def test_receita_por_categoria(pg):
    rows = _consulta(pg, "SELECT categoria, receita FROM fct_receita_categoria ORDER BY receita DESC")
    assert [(r[0], float(r[1])) for r in rows] == [
        ("livros", 230.0),          # dois produtos (p2 e p4) na mesma categoria
        ("eletronicos", 150.0),
        ("casa", 80.0),
        ("Desconhecido", 40.0),     # item de produto fora do cadastro: entra, não some
    ]


def test_receita_reconcilia_com_os_itens(pg):
    mart, itens = _consulta(pg, """
        SELECT (SELECT SUM(receita) FROM fct_receita_categoria), (SELECT SUM(price) FROM stg_itens)""")[0]
    assert mart == itens, f"o mart soma {mart}, os itens somam {itens}: INNER JOIN derruba item órfão"


def test_mart_materializado_como_tabela(pg):
    _consulta(pg, "SELECT 1 FROM fct_receita_categoria LIMIT 0")
    tipo = _consulta(pg, """SELECT table_type FROM information_schema.tables
                            WHERE table_schema = 'm7_ex03' AND table_name = 'fct_receita_categoria'""")
    assert tipo == [("BASE TABLE",)], "mantenha {{ config(materialized='table') }}: marts são lidos muitas vezes"


def test_mart_le_os_staging_com_ref():
    # roda sem bancada: a linhagem stg_* -> fct_* só existe se o mart usa ref(), nunca a fonte crua
    sql = re.sub(r"--.*", "", MODEL.read_text(encoding="utf-8"))
    assert "ref('stg_itens')" in sql.replace('"', "'") and "ref('stg_produtos')" in sql.replace('"', "'"), \
        "leia os dois staging com {{ ref('stg_itens') }} e {{ ref('stg_produtos') }}"
    assert not re.search(r"raw_(itens|produtos)", sql), "o mart não deve ler os seeds crus (raw_*)"
