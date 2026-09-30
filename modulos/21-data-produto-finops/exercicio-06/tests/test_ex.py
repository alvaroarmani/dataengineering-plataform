import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import copy

from solucao import avaliar_produto  # noqa: E402

PRONTO = {
    "dono": "time-vendas@empresa.com",
    "descricao": "Vendas diárias por loja, com devoluções já abatidas.",
    "sla": {"freshness_horas": 24},
    "colunas": [{"nome": "loja_id", "descricao": "Id da loja", "pii": False},
                {"nome": "cpf_gerente", "descricao": "CPF do gerente", "pii": True}],
    "testes": {"unique_loja_dia": True, "not_null_valor": True},
}


def _com(**mudancas):
    p = copy.deepcopy(PRONTO)
    p.update(mudancas)
    return p


def test_produto_completo():
    assert avaliar_produto(PRONTO) == {"pronto": True, "pendencias": [], "nota": 100.0}


def test_dono_so_com_espacos_e_descricao_curta():
    r = avaliar_produto(_com(dono="   ", descricao="vendas"))
    assert r == {"pronto": False, "pendencias": ["descricao", "dono"], "nota": 66.7}


def test_sla_vazio_ou_invalido():
    assert avaliar_produto(_com(sla={}))["pendencias"] == ["sla"]
    assert avaliar_produto(_com(sla={"freshness_horas": 0}))["pendencias"] == ["sla"]
    assert avaliar_produto(_com(sla={"freshness_horas": True}))["pendencias"] == ["sla"]


def test_coluna_sem_descricao_e_sem_marcacao_de_pii():
    cols = copy.deepcopy(PRONTO["colunas"]) + [{"nome": "email_cliente", "descricao": ""}]
    assert avaliar_produto(_com(colunas=cols))["pendencias"] == ["pii_classificada", "schema_documentado"]


def test_testes_falhando_ou_inexistentes():
    assert avaliar_produto(_com(testes={"unique_loja_dia": False}))["pendencias"] == ["testes_passando"]
    assert avaliar_produto(_com(testes={}))["pendencias"] == ["testes_passando"]


def test_produto_vazio():
    r = avaliar_produto({})
    assert r["pronto"] is False and r["nota"] == 0.0 and len(r["pendencias"]) == 6
