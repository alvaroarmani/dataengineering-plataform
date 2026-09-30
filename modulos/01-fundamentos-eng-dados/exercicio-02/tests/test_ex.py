import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import perfil_carga  # noqa: E402


def q(tipo, lidas, agrega=False):
    return {"tipo": tipo, "linhas_lidas": lidas, "agrega": agrega}


APP = [q("INSERT", 0), q("SELECT", 1), q("UPDATE", 1), q("SELECT", 3), q("INSERT", 0),
       q("SELECT", 1), q("SELECT", 20), q("DELETE", 1), q("SELECT", 1), q("SELECT", 2)]
BI = [q("SELECT", 5_000_000, True), q("SELECT", 800_000, True), q("SELECT", 12_000_000, True),
      q("INSERT", 0), q("SELECT", 150)]


def test_banco_do_app_e_oltp():
    assert perfil_carga(APP) == {"classe": "OLTP", "pct_escrita": 0.4, "pct_agregacao": 0.0, "mediana_lidas": 1.0}


def test_warehouse_e_olap():
    assert perfil_carga(BI) == {"classe": "OLAP", "pct_escrita": 0.2, "pct_agregacao": 0.6, "mediana_lidas": 800_000}


def test_relatorio_rodando_no_banco_do_app_vira_misto():
    r = perfil_carga(APP[:6] + [q("SELECT", 2_000, True)] * 5)
    assert r == {"classe": "misto", "pct_escrita": 0.27, "pct_agregacao": 0.45, "mediana_lidas": 3}


def test_fronteiras():
    assert perfil_carga([q("INSERT", 0)] * 3 + [q("SELECT", 100)] * 7)["classe"] == "OLTP"   # 0.3 e 100
    assert perfil_carga([q("SELECT", 10_000)])["classe"] == "OLAP"


def test_invalidos():
    with pytest.raises(ValueError):
        perfil_carga([])
    with pytest.raises(ValueError):
        perfil_carga([q("MERGE", 1)])
