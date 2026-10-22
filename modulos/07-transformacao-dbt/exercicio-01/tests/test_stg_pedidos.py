"""Grader do Exercício 01 (M7) — confere o model `stg_pedidos` construído pelo dbt.

Pré-requisito: rodar `dbt build` (seed + model + testes) na bancada. Ver enunciado.
Os testes de schema do próprio dbt (not_null/unique) já cobrem parte; aqui checamos os
VALORES da transformação (estado limpo, tipos convertidos).
"""
import pytest


def _consulta(pg, sql):
    cur = pg.cursor()
    cur.execute("SET search_path TO m7_ex01")              # o schema do profiles.yml deste exercício
    try:
        cur.execute(sql)
    except Exception as e:  # noqa: BLE001
        pg.rollback()
        if getattr(e, "pgcode", None) != "42P01":    # só "tabela não existe" é skip; coluna faltando é falha
            raise
        pytest.skip(f"stg_pedidos não encontrado ({e}). Rode `dbt build` primeiro.")
    return cur.fetchall()


def test_stg_pedidos_transformacao(pg):
    rows = _consulta(pg, "SELECT pedido_id, cliente, estado, valor FROM stg_pedidos ORDER BY pedido_id")
    assert [(r[0], r[1], r[2], float(r[3])) for r in rows] == [
        (1, "ana", "SP", 100.0),
        (2, "bruno", "RJ", 200.0),
        (3, "caio", "MG", 50.0),
        (4, "ana", "SP", 80.0),
        (5, "duda", "RJ", 1200.5),
    ]


def test_estado_sem_espaco_e_em_maiuscula(pg):
    # ' rj ' no seed: UPPER sozinho vira ' RJ ' e quebra qualquer GROUP BY estado a jusante
    estados = {r[0] for r in _consulta(pg, "SELECT DISTINCT estado FROM stg_pedidos")}
    assert estados == {"SP", "RJ", "MG"}, f"estados obtidos: {sorted(estados)} — use TRIM além de UPPER"


def test_tipos_convertidos(pg):
    _consulta(pg, "SELECT 1 FROM stg_pedidos LIMIT 0")    # skip se o dbt ainda não rodou
    tipos = dict(_consulta(pg, """
        SELECT column_name, data_type FROM information_schema.columns
        WHERE table_name = 'stg_pedidos' AND table_schema = current_schema()"""))
    assert tipos.get("pedido_id") == "integer", f"pedido_id é {tipos.get('pedido_id')}: use cast(id as integer)"
    assert tipos.get("valor") == "numeric", f"valor é {tipos.get('valor')}: use cast(valor_str as numeric)"


def test_pedido_id_unico(pg):
    total, distintos = _consulta(pg, "SELECT COUNT(*), COUNT(DISTINCT pedido_id) FROM stg_pedidos")[0]
    assert total == distintos == 5, "pedido_id deve ser único (grão de 1 linha por pedido), sem perder linhas"
