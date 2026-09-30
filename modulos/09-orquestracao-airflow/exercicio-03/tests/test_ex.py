import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import executar  # noqa: E402

LINHAS = [{"id": i, "valor": i * 10} for i in range(500)]


def test_pipeline_com_referencias():
    tasks = [
        ("extrair", [], lambda x: {"caminho": "s3://raw/vendas/2026-09-30.parquet", "linhas": 500}),
        ("validar", ["extrair"], lambda x: x["extrair"]["linhas"] > 0),
        ("carregar", ["extrair", "validar"], lambda x: {"tabela": "stg.vendas", "ok": x["validar"]}),
    ]
    assert executar(tasks) == {
        "extrair": {"caminho": "s3://raw/vendas/2026-09-30.parquet", "linhas": 500},
        "validar": True,
        "carregar": {"tabela": "stg.vendas", "ok": True}}


def test_cada_task_so_ve_os_proprios_upstreams():
    vistos = {}
    tasks = [("a", [], lambda x: 1), ("b", [], lambda x: 2),
             ("c", ["b"], lambda x: vistos.setdefault("c", sorted(x)) and 3)]
    executar(tasks)
    assert vistos["c"] == ["b"]


def test_dataset_por_xcom_estoura():
    tasks = [("extrair", [], lambda x: LINHAS), ("somar", ["extrair"], lambda x: sum(r["valor"] for r in x["extrair"]))]
    with pytest.raises(ValueError, match="extrair"):
        executar(tasks)
    assert executar(tasks, limite_bytes=100_000)["somar"] == 1_247_500


def test_upstream_que_nao_rodou():
    with pytest.raises(KeyError):
        executar([("b", ["a"], lambda x: 1), ("a", [], lambda x: 0)])
