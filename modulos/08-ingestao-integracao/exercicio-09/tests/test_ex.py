import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import aplicar_cdc  # noqa: E402

ESTADO = {"tabela": {1: "ana", 2: "bia"}, "ultimo_lsn": 100}


def test_fora_de_ordem_e_aplicado_pelo_lsn():
    eventos = [{"lsn": 103, "op": "D", "chave": 2},
               {"lsn": 101, "op": "U", "chave": 1, "valor": "ana maria"},
               {"lsn": 102, "op": "I", "chave": 3, "valor": "caio"}]
    r = aplicar_cdc(ESTADO, eventos)
    assert r["tabela"] == {1: "ana maria", 3: "caio"} and r["ultimo_lsn"] == 103
    assert (r["aplicados"], r["ignorados"], r["anomalias"]) == (3, 0, [])


def test_update_depois_do_delete_na_ordem_certa():
    eventos = [{"lsn": 102, "op": "U", "chave": 2, "valor": "bia 2"}, {"lsn": 101, "op": "D", "chave": 2}]
    r = aplicar_cdc(ESTADO, eventos)
    assert r["tabela"] == {1: "ana", 2: "bia 2"} and r["anomalias"] == [(102, "U_inexistente")]


def test_reentrega_e_idempotente():
    eventos = [{"lsn": 99, "op": "D", "chave": 1},              # já aplicado antes
               {"lsn": 101, "op": "I", "chave": 4, "valor": "davi"},
               {"lsn": 101, "op": "I", "chave": 4, "valor": "davi"}]   # repetido no lote
    r = aplicar_cdc(ESTADO, eventos)
    assert r["tabela"] == {1: "ana", 2: "bia", 4: "davi"}
    assert (r["aplicados"], r["ignorados"]) == (1, 2)
    assert aplicar_cdc({"tabela": r["tabela"], "ultimo_lsn": r["ultimo_lsn"]}, eventos)["aplicados"] == 0


def test_anomalias_e_entrada_intacta():
    eventos = [{"lsn": 101, "op": "I", "chave": 1, "valor": "outra ana"}, {"lsn": 102, "op": "D", "chave": 9}]
    r = aplicar_cdc(ESTADO, eventos)
    assert r["anomalias"] == [(101, "I_existente"), (102, "D_inexistente")]
    assert ESTADO == {"tabela": {1: "ana", 2: "bia"}, "ultimo_lsn": 100}


def test_op_desconhecida():
    with pytest.raises(ValueError):
        aplicar_cdc(ESTADO, [{"lsn": 101, "op": "X", "chave": 1}])
