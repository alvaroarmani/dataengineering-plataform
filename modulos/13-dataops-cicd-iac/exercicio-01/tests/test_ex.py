import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import avaliar_pr  # noqa: E402

REGRAS = {"checks_obrigatorios": ["lint", "dbt-build"], "aprovacoes_min": 1,
          "codeowners": {"models/finance/": "carla", "infra/": "diego"}}


def _pr(**kw):
    base = {"autor": "ana", "checks": [("lint", "pass"), ("dbt-build", "pass")],
            "aprovacoes": ["bruno"], "arquivos": ["models/marketing/campanhas.sql"], "atualizado": True}
    base.update(kw)
    return base


def test_pr_ok():
    assert avaliar_pr(_pr(), REGRAS) == {"pode": True, "bloqueios": []}


def test_check_reexecutado_vale_o_ultimo():
    assert avaliar_pr(_pr(checks=[("lint", "pass"), ("dbt-build", "fail"), ("dbt-build", "pass")]), REGRAS)["pode"]
    r = avaliar_pr(_pr(checks=[("lint", "pass"), ("dbt-build", "pass"), ("dbt-build", "fail")]), REGRAS)
    assert r["bloqueios"] == ["check:dbt-build"]


def test_check_obrigatorio_ausente_e_autoaprovacao():
    r = avaliar_pr(_pr(checks=[("lint", "pass")], aprovacoes=["ana", "ana"]), REGRAS)
    assert r == {"pode": False, "bloqueios": ["aprovacoes:0/1", "check:dbt-build"]}


def test_codeowner():
    arquivos = ["models/finance/receita.sql", "README.md"]
    assert avaliar_pr(_pr(arquivos=arquivos), REGRAS)["bloqueios"] == ["codeowner:carla"]
    assert avaliar_pr(_pr(arquivos=arquivos, aprovacoes=["carla"]), REGRAS)["pode"] is True


def test_dono_como_autor_ainda_precisa_de_outro_revisor():
    r = avaliar_pr(_pr(autor="carla", arquivos=["models/finance/x.sql"], aprovacoes=[]), REGRAS)
    assert r["bloqueios"] == ["aprovacoes:0/1"]


def test_todos_os_bloqueios_juntos():
    r = avaliar_pr(_pr(checks=[], aprovacoes=[], arquivos=["infra/main.tf"], atualizado=False), REGRAS)
    assert r["bloqueios"] == ["aprovacoes:0/1", "check:dbt-build", "check:lint", "codeowner:diego", "desatualizado"]
