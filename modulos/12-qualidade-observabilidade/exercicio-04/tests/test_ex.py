import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import relatorio_dominio  # noqa: E402

PERMITIDOS = ["pago", "cancelado", "enviado"]


def test_separa_cosmetico_de_invalido():
    valores = ["pago", " Pago", "PAGO", "pg", "enviado", None, "cancelado ", "pg", "???"]
    assert relatorio_dominio(valores, PERMITIDOS) == {
        "validos": 2,
        "corrigiveis": {" Pago": 1, "PAGO": 1, "cancelado ": 1},
        "invalidos": {"pg": 2, None: 1, "???": 1},
        "pct_invalido": 44.44,
    }


def test_tudo_valido():
    r = relatorio_dominio(["pago", "pago", "enviado"], PERMITIDOS)
    assert r == {"validos": 3, "corrigiveis": {}, "invalidos": {}, "pct_invalido": 0.0}


def test_numeros_no_dominio():
    assert relatorio_dominio([1, 2, 3, 2], [1, 2])["invalidos"] == {3: 1}


def test_lista_vazia():
    assert relatorio_dominio([], PERMITIDOS)["pct_invalido"] == 0.0


def test_permitidos_tambem_sao_normalizados():
    r = relatorio_dominio(["pago"], ["PAGO "])
    assert r["validos"] == 0 and r["corrigiveis"] == {"pago": 1}
