import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import copy

from solucao import merge_incremental  # noqa: E402

DESTINO = [{"id": 1, "status": "pago", "updated_at": 5},
           {"id": 2, "status": "novo", "updated_at": 5},
           {"id": 3, "status": "novo", "updated_at": 4}]


def test_upsert_e_dado_atrasado():
    lote = [{"id": 2, "status": "pago", "updated_at": 8},
            {"id": 4, "status": "novo", "updated_at": 7},
            {"id": 1, "status": "novo", "updated_at": 2}]           # atrasado: não volta para "novo"
    assert merge_incremental(DESTINO, lote, "id") == [
        {"id": 1, "status": "pago", "updated_at": 5}, {"id": 2, "status": "pago", "updated_at": 8},
        {"id": 3, "status": "novo", "updated_at": 4}, {"id": 4, "status": "novo", "updated_at": 7}]


def test_duplicata_no_lote_fica_a_mais_recente():
    lote = [{"id": 3, "status": "enviado", "updated_at": 9},
            {"id": 3, "status": "pago", "updated_at": 6},
            {"id": 5, "status": "a", "updated_at": 1},
            {"id": 5, "status": "b", "updated_at": 1}]               # empate: vale o último
    r = {x["id"]: x["status"] for x in merge_incremental(DESTINO, lote, "id")}
    assert r[3] == "enviado" and r[5] == "b"


def test_exclusao_logica():
    lote = [{"id": 2, "updated_at": 6, "_deleted": True},
            {"id": 9, "updated_at": 6, "_deleted": True},              # apagar o que nem existe: nada
            {"id": 1, "updated_at": 1, "_deleted": True}]              # exclusão atrasada: ignorada
    assert [x["id"] for x in merge_incremental(DESTINO, lote, "id")] == [1, 3]


def test_mesmo_updated_at_aplica_e_nao_muta_entrada():
    antes = copy.deepcopy(DESTINO)
    r = merge_incremental(DESTINO, [{"id": 1, "status": "estornado", "updated_at": 5}], "id")
    assert r[0]["status"] == "estornado"
    assert DESTINO == antes


def test_idempotente():
    lote = [{"id": 2, "status": "pago", "updated_at": 8}]
    uma = merge_incremental(DESTINO, lote, "id")
    assert merge_incremental(uma, lote, "id") == uma
