import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import executar_workflow  # noqa: E402

JOBS = {
    "lint": [],
    "dbt-build": ["lint"],
    "dbt-test": ["dbt-build"],
    "docs": ["lint"],
    "deploy": ["dbt-test", "docs"],
}
TUDO_OK = {j: True for j in JOBS}


def test_tudo_verde():
    r = executar_workflow(JOBS, TUDO_OK)
    assert r["conclusao"] == "success" and set(r["jobs"].values()) == {"success"}


def test_falha_propaga_skip_mas_nao_para_o_independente():
    r = executar_workflow(JOBS, {**TUDO_OK, "dbt-build": False})
    assert r == {"jobs": {"dbt-build": "failure", "dbt-test": "skipped", "deploy": "skipped",
                          "docs": "success", "lint": "success"}, "conclusao": "failure"}


def test_falha_na_raiz_pula_tudo():
    r = executar_workflow(JOBS, {**TUDO_OK, "lint": False})
    assert r["jobs"] == {"dbt-build": "skipped", "dbt-test": "skipped", "deploy": "skipped",
                         "docs": "skipped", "lint": "failure"}


def test_resultado_de_job_pulado_nao_importa():
    # deploy "falharia", mas nem roda: a conclusão vem do dbt-test
    r = executar_workflow(JOBS, {**TUDO_OK, "dbt-test": False, "deploy": False})
    assert r["jobs"]["deploy"] == "skipped" and r["conclusao"] == "failure"


def test_ciclo_e_dependencia_inexistente():
    with pytest.raises(ValueError):
        executar_workflow({"a": ["b"], "b": ["a"]}, {"a": True, "b": True})
    with pytest.raises(ValueError):
        executar_workflow({"a": ["x"]}, {"a": True})
