import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import agendar  # noqa: E402

NOS = {"no-a": (4.0, 16), "no-b": (8.0, 32), "no-c": (4.0, 8)}


def test_espalha_pela_fracao_livre():
    r = agendar([("api-1", 1.0, 2), ("api-2", 1.0, 2), ("api-3", 1.0, 2)], NOS)
    assert r["alocacao"] == {"api-1": "no-b", "api-2": "no-a", "api-3": "no-b"}   # api-2: empate em 75% -> nome


def test_memoria_tambem_filtra():
    r = agendar([("spark-driver", 1.0, 12)], NOS)
    assert r["alocacao"] == {"spark-driver": "no-b"}
    r2 = agendar([("x", 1.0, 20)], {"no-a": (4.0, 16), "no-c": (4.0, 8)})
    assert r2["alocacao"] == {"x": "Pending"}


def test_pending_quando_nao_cabe_e_livre_final():
    pods = [("etl-1", 6.0, 20), ("etl-2", 3.0, 8), ("etl-3", 3.0, 8), ("etl-4", 3.0, 8)]
    r = agendar(pods, NOS)
    assert r["alocacao"] == {"etl-1": "no-b", "etl-2": "no-a", "etl-3": "no-c", "etl-4": "Pending"}
    assert r["livre"] == {"no-a": (1.0, 8), "no-b": (2.0, 12), "no-c": (1.0, 0)}


def test_request_invalido():
    with pytest.raises(ValueError):
        agendar([("x", 0, 1)], NOS)
