import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import plano  # noqa: E402

IMUTAVEIS = {"bucket": ["regiao", "nome"], "dataset": ["localizacao"]}
ATUAL = {
    "raw": {"tipo": "bucket", "nome": "empresa-raw", "regiao": "us", "descricao": "dados crus"},
    "tmp": {"tipo": "bucket", "nome": "empresa-tmp", "regiao": "us"},
    "dw": {"tipo": "dataset", "localizacao": "US", "expiracao_dias": 0, "prevent_destroy": True},
}


def test_atualizar_no_lugar():
    desejado = {**ATUAL, "raw": {**ATUAL["raw"], "descricao": "zona bronze", "versionamento": True}}
    assert plano(ATUAL, desejado, IMUTAVEIS) == {
        "criar": [], "atualizar": {"raw": ["descricao", "versionamento"]}, "substituir": [], "destruir": []}


def test_mudar_regiao_forca_substituicao():
    desejado = {**ATUAL, "tmp": {**ATUAL["tmp"], "regiao": "southamerica-east1"}}
    assert plano(ATUAL, desejado, IMUTAVEIS)["substituir"] == ["tmp"]


def test_criar_e_destruir():
    desejado = {"raw": ATUAL["raw"], "dw": ATUAL["dw"], "logs": {"tipo": "bucket", "nome": "empresa-logs", "regiao": "us"}}
    assert plano(ATUAL, desejado, IMUTAVEIS) == {"criar": ["logs"], "atualizar": {}, "substituir": [], "destruir": ["tmp"]}


def test_prevent_destroy_barra_destruicao_e_substituicao():
    with pytest.raises(ValueError):
        plano(ATUAL, {"raw": ATUAL["raw"], "tmp": ATUAL["tmp"]}, IMUTAVEIS)
    with pytest.raises(ValueError):
        plano(ATUAL, {**ATUAL, "dw": {**ATUAL["dw"], "localizacao": "EU"}}, IMUTAVEIS)


def test_prevent_destroy_permite_atualizar():
    r = plano(ATUAL, {**ATUAL, "dw": {**ATUAL["dw"], "expiracao_dias": 90}}, IMUTAVEIS)
    assert r["atualizar"] == {"dw": ["expiracao_dias"]}


def test_sem_mudancas_e_troca_de_tipo():
    assert plano(ATUAL, ATUAL, IMUTAVEIS) == {"criar": [], "atualizar": {}, "substituir": [], "destruir": []}
    desejado = {**ATUAL, "tmp": {"tipo": "dataset", "localizacao": "US"}}
    assert plano(ATUAL, desejado, IMUTAVEIS)["substituir"] == ["tmp"]
