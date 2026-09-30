import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import conciliar_schema  # noqa: E402

CONTRATO = {"id": {"tipo": "int", "nulo": False}, "valor": {"tipo": "float", "nulo": False},
            "cupom": {"tipo": "str", "nulo": True}, "pago": {"tipo": "bool", "nulo": False}}


def test_registro_perfeito():
    r = conciliar_schema(CONTRATO, {"id": 1, "valor": 9.9, "cupom": None, "pago": True})
    assert r == {"decisao": "aceitar", "faltando": [], "extras": [], "incompativeis": [], "promovidas": []}


def test_mudancas_compativeis_geram_aviso():
    r = conciliar_schema(CONTRATO, {"id": 1, "valor": 10, "cupom": "X", "pago": False, "canal": "app"})
    assert r["decisao"] == "aceitar_com_aviso" and r["promovidas"] == ["valor"] and r["extras"] == ["canal"]


def test_mudancas_incompativeis_rejeitam():
    r = conciliar_schema(CONTRATO, {"id": "1", "valor": None, "pago": True, "canal": "app"})
    assert r == {"decisao": "rejeitar", "faltando": ["cupom"], "extras": ["canal"],
                 "incompativeis": ["id", "valor"], "promovidas": []}


def test_bool_nao_e_numero_e_float_nao_vira_int():
    r = conciliar_schema(CONTRATO, {"id": 1.0, "valor": True, "cupom": None, "pago": True})
    assert r["incompativeis"] == ["id", "valor"]


def test_bool_errado_no_campo_bool():
    assert conciliar_schema(CONTRATO, {"id": 1, "valor": 1.0, "cupom": None, "pago": 1})["incompativeis"] == ["pago"]
