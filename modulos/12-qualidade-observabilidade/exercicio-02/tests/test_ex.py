import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import validar, validar_lote  # noqa: E402

CONTRATO = {
    "id": {"tipo": "int", "obrigatorio": True, "nulo": False},
    "valor": {"tipo": "float", "obrigatorio": True, "nulo": False},
    "cupom": {"tipo": "str", "obrigatorio": False, "nulo": True},
    "pago": {"tipo": "bool", "obrigatorio": True, "nulo": False},
}


def test_registro_valido():
    assert validar({"id": 1, "valor": 10.5, "cupom": "X", "pago": True}, CONTRATO) == []


def test_float_aceita_int_e_opcional_pode_faltar():
    assert validar({"id": 1, "valor": 10, "pago": False}, CONTRATO) == []


def test_bool_nao_e_int():
    assert validar({"id": True, "valor": 1.0, "pago": True}, CONTRATO) == ["id:tipo"]
    assert validar({"id": 1, "valor": False, "pago": True}, CONTRATO) == ["valor:tipo"]


def test_varias_violacoes_ordenadas():
    r = {"valor": None, "cupom": None, "pago": "sim", "canal": "app"}
    assert validar(r, CONTRATO) == ["canal:nao_previsto", "id:ausente", "pago:tipo", "valor:nulo"]


def test_string_numerica_nao_e_numero():
    assert validar({"id": "7", "valor": "9.90", "pago": True}, CONTRATO) == ["id:tipo", "valor:tipo"]


def test_contrato_com_tipo_desconhecido():
    with pytest.raises(ValueError):
        validar({"x": 1}, {"x": {"tipo": "decimal", "obrigatorio": True, "nulo": False}})


def test_resumo_do_lote():
    lote = [{"id": 1, "valor": 2.0, "pago": True},
            {"id": "2", "valor": 2.0, "pago": True},
            {"id": 3, "pago": True},
            {"id": "4", "valor": None, "pago": True}]
    assert validar_lote(lote, CONTRATO) == {
        "validos": 1, "invalidos": 3,
        "violacoes": {"id:tipo": 2, "valor:ausente": 1, "valor:nulo": 1}}
