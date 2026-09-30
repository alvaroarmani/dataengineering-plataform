import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import minutos_indisponiveis, orcamento_de_erro  # noqa: E402

INCIDENTES = [
    ("2026-09-01 10:00", "2026-09-01 10:20"),   # job de carga falhou
    ("2026-09-01 10:10", "2026-09-01 10:30"),   # dashboard sem dado (sobrepõe o anterior)
    ("2026-09-15 08:00", "2026-09-15 08:05"),
]


def test_uniao_de_intervalos():
    assert minutos_indisponiveis(INCIDENTES) == 35.0                 # não 45
    assert minutos_indisponiveis([("2026-09-01 10:00", "2026-09-01 11:00"),
                                  ("2026-09-01 10:15", "2026-09-01 10:20")]) == 60.0   # contido
    assert minutos_indisponiveis([]) == 0.0


def test_intervalos_encostados_e_fora_de_ordem():
    assert minutos_indisponiveis([("2026-09-02 09:10", "2026-09-02 09:20"),
                                  ("2026-09-02 09:00", "2026-09-02 09:10")]) == 20.0


def test_orcamento_ainda_disponivel():
    assert orcamento_de_erro(99.9, 30, INCIDENTES) == {
        "permitido_min": 43.2, "consumido_min": 35.0, "restante_min": 8.2,
        "queimado_pct": 81.02, "cumpre": True}


def test_orcamento_estourado():
    r = orcamento_de_erro(99.9, 30, INCIDENTES + [("2026-09-20 00:00", "2026-09-20 00:10")])
    assert r["cumpre"] is False and r["restante_min"] == -1.8 and r["queimado_pct"] == 104.17


def test_slo_mais_frouxo():
    assert orcamento_de_erro(99.0, 30, INCIDENTES)["permitido_min"] == 432.0


def test_incidente_invertido():
    with pytest.raises(ValueError):
        minutos_indisponiveis([("2026-09-01 10:00", "2026-09-01 09:00")])
