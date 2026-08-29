"""Grader do Exercício 05 (M7) — confere que o teste `relationships` foi declarado.

Este grader lê o schema.yml (não precisa da bancada). Na bancada, `dbt build` roda o teste
de verdade contra os dados (integridade referencial real).
"""
from pathlib import Path

import yaml

SCHEMA = Path(__file__).resolve().parents[1] / "projeto_dbt" / "models" / "schema.yml"


def _coluna(modelo_nome, coluna_nome):
    d = yaml.safe_load(SCHEMA.read_text(encoding="utf-8"))
    modelo = next(m for m in d["models"] if m["name"] == modelo_nome)
    return next(c for c in modelo["columns"] if c["name"] == coluna_nome)


def test_relationships_declarado_em_fct():
    col = _coluna("fct_itens", "produto_id")
    tests = col.get("tests") or []
    rels = [t for t in tests if isinstance(t, dict) and "relationships" in t]
    assert rels, "adicione um teste 'relationships' em fct_itens.produto_id"
    r = rels[0]["relationships"]
    assert "dim_produto" in str(r.get("to", "")), "relationships.to deve apontar para ref('dim_produto')"
    assert r.get("field") == "produto_id", "relationships.field deve ser produto_id"


def test_dim_mantem_chave_testada():
    # a integridade só vale se a chave da dimensão é única e não-nula (já vem pronto)
    col = _coluna("dim_produto", "produto_id")
    tests = [t for t in (col.get("tests") or [])]
    assert "not_null" in tests and "unique" in tests
