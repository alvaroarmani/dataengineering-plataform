import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import hpa  # noqa: E402


def test_escala_para_cima():
    assert hpa(2, {"cpu": (90, 50)}, 1, 10) == {"replicas": 4, "motivo": "cpu"}


def test_tolerancia_evita_oscilacao():
    assert hpa(4, {"cpu": (54, 50)}, 1, 10) == {"replicas": 4, "motivo": "cpu"}      # razão 1,08
    assert hpa(4, {"cpu": (56, 50)}, 1, 10) == {"replicas": 5, "motivo": "cpu"}      # razão 1,12
    assert hpa(4, {"cpu": (46, 50)}, 1, 10) == {"replicas": 4, "motivo": "cpu"}      # razão 0,92


def test_varias_metricas_vence_a_maior():
    r = hpa(4, {"cpu": (30, 60), "fila": (900, 100)}, 1, 50)
    assert r == {"replicas": 36, "motivo": "fila"}          # CPU pediria 2; a fila pede 36


def test_limites():
    assert hpa(4, {"cpu": (10, 50)}, 2, 10) == {"replicas": 2, "motivo": "limite_min"}
    assert hpa(8, {"cpu": (100, 50)}, 1, 10) == {"replicas": 10, "motivo": "limite_max"}


def test_configuracao_invalida():
    with pytest.raises(ValueError):
        hpa(2, {}, 1, 5)
    with pytest.raises(ValueError):
        hpa(2, {"cpu": (50, 0)}, 1, 5)
    with pytest.raises(ValueError):
        hpa(2, {"cpu": (50, 50)}, 6, 5)
