import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import casa, entregar  # noqa: E402


@pytest.mark.parametrize("padrao, tipo, ok", [
    ("pedido.criado", "pedido.criado", True),
    ("pedido.*", "pedido.criado", True),
    ("pedido.*", "pedido", False),                   # * exige um segmento
    ("pedido.*", "pedido.item.adicionado", False),
    ("pedido.#", "pedido", True),                     # # aceita zero segmentos
    ("pedido.#", "pedido.item.adicionado", True),
    ("#", "qualquer.coisa", True),
    ("*.aprovado", "pagamento.aprovado", True),
    ("#.aprovado", "pagamento.pix.aprovado", True),
    ("pagamento.*", "pedido.criado", False),
])
def test_casa(padrao, tipo, ok):
    assert casa(padrao, tipo) is ok


ASSINATURAS = {
    "faturamento": ["pedido.criado", "pedido.cancelado"],
    "antifraude": ["pagamento.#", "pedido.criado"],
    "estoque": ["pedido.*"],
    "auditoria_pix": ["#.pix.#"],
}


def test_entrega_com_fan_out_e_dlq():
    eventos = [(1, "pedido.criado"), (2, "pagamento.pix.aprovado"), (3, "pedido.cancelado"),
               (4, "cliente.criado"), (5, "pedido.criado.v2")]
    assert entregar(eventos, ASSINATURAS) == {
        "faturamento": [1, 3], "antifraude": [1, 2], "estoque": [1, 3],
        "auditoria_pix": [2], "DLQ": [4, 5]}


def test_varios_padroes_do_mesmo_consumidor_entregam_uma_vez():
    r = entregar([(9, "pedido.criado")], {"x": ["pedido.*", "#", "pedido.criado"]})
    assert r == {"x": [9], "DLQ": []}
