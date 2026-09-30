import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import estado_task, executar_dag  # noqa: E402


@pytest.mark.parametrize("regra, ups, esperado", [
    ("all_success", ["success", "success"], "run"),
    ("all_success", ["success", "failed"], "upstream_failed"),
    ("all_success", ["success", "skipped"], "skipped"),
    ("all_done", ["failed", "upstream_failed"], "run"),
    ("one_failed", ["success", "upstream_failed"], "run"),
    ("one_failed", ["success", "success"], "skipped"),
    ("none_failed", ["success", "skipped"], "run"),
    ("none_failed", ["failed"], "upstream_failed"),
    ("all_success", [], "run"),
])
def test_estado_task(regra, ups, esperado):
    assert estado_task(regra, ups) == esperado


DAG = {
    "extrair": {"upstream": [], "regra": "all_success"},
    "transformar": {"upstream": ["extrair"], "regra": "all_success"},
    "carregar": {"upstream": ["transformar"], "regra": "all_success"},
    "limpar_tmp": {"upstream": ["carregar"], "regra": "all_done"},
    "alertar": {"upstream": ["extrair", "transformar", "carregar"], "regra": "one_failed"},
}


def test_falha_no_meio():
    r = executar_dag(DAG, {"transformar": False})
    assert r == {"estados": {"alertar": "success", "carregar": "upstream_failed", "extrair": "success",
                             "limpar_tmp": "success", "transformar": "failed"}, "run": "failed"}


def test_tudo_certo_alerta_e_pulado():
    r = executar_dag(DAG, {})
    assert r["estados"]["alertar"] == "skipped" and r["estados"]["limpar_tmp"] == "success" and r["run"] == "success"


def test_regra_desconhecida():
    with pytest.raises(ValueError):
        estado_task("sometimes", ["success"])
