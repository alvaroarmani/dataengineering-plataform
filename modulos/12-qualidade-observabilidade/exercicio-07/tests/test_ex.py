import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import decidir_alerta  # noqa: E402

CRITICOS = {"freshness_pedidos", "unique_pedido_id"}


def test_falha_critica_chama_plantao():
    r = decidir_alerta([("freshness_pedidos", "fail"), ("accepted_status", "warn")], CRITICOS)
    assert r == {"acao": "plantao", "falhas": ["freshness_pedidos"], "avisos": ["accepted_status"]}


def test_falha_comum_vai_para_o_canal():
    assert decidir_alerta([("not_null_email", "fail"), ("unique_pedido_id", "pass")], CRITICOS)["acao"] == "canal"


def test_avisos_acumulados():
    tres = [("a", "warn"), ("b", "warn"), ("c", "warn")]
    assert decidir_alerta(tres, CRITICOS)["acao"] == "canal"
    assert decidir_alerta(tres[:2], CRITICOS)["acao"] == "nada"
    assert decidir_alerta(tres[:2], CRITICOS, limite_avisos=2)["acao"] == "canal"


def test_reexecucao_vale_o_ultimo_status():
    r = decidir_alerta([("unique_pedido_id", "fail"), ("unique_pedido_id", "pass")], CRITICOS)
    assert r == {"acao": "nada", "falhas": [], "avisos": []}


def test_tudo_passando_e_vazio():
    assert decidir_alerta([("x", "pass")], CRITICOS)["acao"] == "nada"
    assert decidir_alerta([], CRITICOS)["acao"] == "nada"


def test_status_invalido():
    with pytest.raises(ValueError):
        decidir_alerta([("x", "error")], CRITICOS)
