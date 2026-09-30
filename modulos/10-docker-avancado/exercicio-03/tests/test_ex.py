import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import subir_stack  # noqa: E402

STACK = {
    "postgres": {"inicio_seg": 2, "health_seg": 8, "depende": {}},
    "minio": {"inicio_seg": 1, "health_seg": 3, "depende": {}},
    "airflow_init": {"inicio_seg": 15, "health_seg": None, "depende": {"postgres": "service_healthy"}},
    "airflow_web": {"inicio_seg": 5, "health_seg": 20, "depende": {"airflow_init": "service_started",
                                                                   "postgres": "service_healthy"}},
    "jupyter": {"inicio_seg": 3, "health_seg": None, "depende": {"minio": "service_started"}},
}


def test_tempos_do_stack():
    r = subir_stack(STACK)
    assert r["iniciado"] == {"airflow_init": 25, "airflow_web": 30, "jupyter": 4, "minio": 1, "postgres": 2}
    assert r["saudavel"]["airflow_web"] == 50 and r["pronto_em"] == 50


def test_service_started_nao_espera_o_banco_ficar_pronto():
    stack = {"postgres": {"inicio_seg": 2, "health_seg": 8, "depende": {}},
             "etl": {"inicio_seg": 1, "health_seg": None, "depende": {"postgres": "service_started"}}}
    assert subir_stack(stack)["iniciado"]["etl"] == 3        # o banco só estaria pronto em 10


def test_sem_dependencias():
    assert subir_stack({"a": {"inicio_seg": 4, "health_seg": 1, "depende": {}}})["pronto_em"] == 5


@pytest.mark.parametrize("stack", [
    {"a": {"inicio_seg": 1, "health_seg": None, "depende": {"b": "service_started"}}},
    {"a": {"inicio_seg": 1, "health_seg": None, "depende": {}},
     "b": {"inicio_seg": 1, "health_seg": None, "depende": {"a": "service_healthy"}}},
    {"a": {"inicio_seg": 1, "health_seg": 1, "depende": {"b": "service_started"}},
     "b": {"inicio_seg": 1, "health_seg": 1, "depende": {"a": "service_started"}}},
])
def test_configuracoes_invalidas(stack):
    with pytest.raises(ValueError):
        subir_stack(stack)
