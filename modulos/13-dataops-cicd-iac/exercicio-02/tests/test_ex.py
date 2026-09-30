import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import alvo_de_deploy  # noqa: E402


def test_ambientes_fixos():
    assert alvo_de_deploy("main", "ana") == {"ambiente": "prod", "schema": "analytics"}
    assert alvo_de_deploy("develop", "ana") == {"ambiente": "staging", "schema": "analytics_staging"}


@pytest.mark.parametrize("branch, usuario, schema", [
    ("feature/nova-metrica", "ana", "dev_ana_nova_metrica"),
    ("feature/Nova Métrica de Vendas!", "Ana", "dev_ana_nova_metrica_de_vendas"),
    ("fix/JIRA-123/corrige_nulos", "joão.silva", "dev_joao_silva_jira_123_corrige_nulos"),
    ("feature/" + "x" * 40, "ana", "dev_ana_" + "x" * 30),
    ("feature/modelo de receita recorrentes mensal", "ana", "dev_ana_modelo_de_receita_recorrentes"),
])
def test_schema_de_dev(branch, usuario, schema):
    assert alvo_de_deploy(branch, usuario) == {"ambiente": "dev", "schema": schema}


def test_dois_devs_no_mesmo_branch_nao_colidem():
    assert alvo_de_deploy("feature/x", "ana") != alvo_de_deploy("feature/x", "bruno")


@pytest.mark.parametrize("branch, usuario", [
    ("hotfix/urgente", "ana"),        # padrão não suportado
    ("feature/", "ana"),
    ("feature/!!!", "ana"),           # vazio depois de normalizar
    ("feature/x", ""),
    ("Main", "ana"),                  # case importa no nome do branch
])
def test_invalidos(branch, usuario):
    with pytest.raises(ValueError):
        alvo_de_deploy(branch, usuario)
