import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import gargalo, snapshot_acumulado  # noqa: E402

PEDIDOS = [
    {"pedido_id": 3, "criado": "2026-03-01"},
    {"pedido_id": 1, "criado": "2026-03-01", "pago": "2026-03-02", "enviado": "2026-03-05", "entregue": "2026-03-10"},
    {"pedido_id": 2, "criado": "2026-03-02", "pago": "2026-03-04"},
    {"pedido_id": 4, "criado": "2026-03-03", "pago": "2026-03-03", "enviado": "2026-03-09", "entregue": "2026-03-11"},
    {"pedido_id": 5, "criado": "2026-03-05", "pago": "2026-03-08", "enviado": "2026-03-06"},   # enviado antes de pago
    {"pedido_id": 6, "criado": "2026-03-06", "entregue": "2026-03-12"},                        # marcos perdidos
]


def test_linha_completa():
    s = snapshot_acumulado(PEDIDOS, "2026-03-15")
    assert s[0] == {"pedido_id": 1, "status": "entregue", "dias_pago": 1, "dias_envio": 3, "dias_entrega": 5,
                    "dias_total": 9, "dias_em_aberto": None, "inconsistente": False}


def test_pedidos_em_aberto_e_ordem():
    s = snapshot_acumulado(PEDIDOS, "2026-03-15")
    assert [l["pedido_id"] for l in s] == [1, 2, 3, 4, 5, 6]
    assert [(l["status"], l["dias_em_aberto"]) for l in s] == [
        ("entregue", None), ("pago", 13), ("criado", 14), ("entregue", None), ("enviado", 10), ("entregue", None)]


def test_marcos_ausentes_e_inconsistentes():
    s = {l["pedido_id"]: l for l in snapshot_acumulado(PEDIDOS, "2026-03-15")}
    assert s[6]["dias_total"] == 6 and s[6]["dias_entrega"] is None
    assert s[5]["inconsistente"] is True and s[5]["dias_envio"] == -2


def test_gargalo_ignora_inconsistentes():
    assert gargalo(snapshot_acumulado(PEDIDOS, "2026-03-15")) == ("dias_envio", 4.5)


def test_erros():
    with pytest.raises(ValueError):
        snapshot_acumulado([{"pedido_id": 9, "pago": "2026-03-01"}], "2026-03-15")
    with pytest.raises(ValueError):
        gargalo(snapshot_acumulado([{"pedido_id": 1, "criado": "2026-03-01"}], "2026-03-02"))
