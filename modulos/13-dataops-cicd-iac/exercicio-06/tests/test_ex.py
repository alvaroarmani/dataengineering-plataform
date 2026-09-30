import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import detectar_drift, resumo_plano  # noqa: E402


def test_resumo_conta_substituicao_duas_vezes():
    p = {"criar": ["logs"], "atualizar": {"raw": ["descricao"]}, "substituir": ["tmp"], "destruir": ["velho"]}
    assert resumo_plano(p) == "Plan: 2 to add, 1 to change, 2 to destroy."


def test_resumo_sem_mudancas():
    assert resumo_plano({"criar": [], "atualizar": {}, "substituir": [], "destruir": []}) == "No changes."


def test_resumo_so_atualizacao():
    p = {"criar": [], "atualizar": {"a": ["x"], "b": ["y"]}, "substituir": [], "destruir": []}
    assert resumo_plano(p) == "Plan: 0 to add, 2 to change, 0 to destroy."


ESTADO = {
    "raw": {"regiao": "us", "versionamento": True},
    "dw": {"localizacao": "US", "expiracao_dias": 0},
    "tmp": {"regiao": "us"},
}


def test_drift():
    real = {
        "raw": {"regiao": "us", "versionamento": False},              # desligaram no console
        "dw": {"localizacao": "US", "expiracao_dias": 0, "rotulo": "x"},
        "bucket_teste_do_joao": {"regiao": "us"},                     # criado na mão
    }
    assert detectar_drift(ESTADO, real) == {
        "alterados": {"dw": ["rotulo"], "raw": ["versionamento"]},
        "nao_gerenciados": ["bucket_teste_do_joao"],
        "sumidos": ["tmp"]}


def test_sem_drift():
    assert detectar_drift(ESTADO, ESTADO) == {"alterados": {}, "nao_gerenciados": [], "sumidos": []}
