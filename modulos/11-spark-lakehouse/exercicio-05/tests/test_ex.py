import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import estrategia_join  # noqa: E402


def test_grande_com_pequena():
    assert estrategia_join(1_000_000, 8) == {"estrategia": "broadcast_hash", "broadcast": "direita", "lados_com_shuffle": 0}


def test_pequena_acima_do_limite_vira_sort_merge():
    assert estrategia_join(1_000_000, 50)["estrategia"] == "sort_merge"
    assert estrategia_join(1_000_000, 50, limite_mb=64)["broadcast"] == "direita"   # subir o limite resolve


def test_left_join_nao_faz_broadcast_da_esquerda():
    r = estrategia_join(5, 1_000_000, tipo="left")
    assert r == {"estrategia": "sort_merge", "broadcast": None, "lados_com_shuffle": 2}
    assert estrategia_join(5, 1_000_000, tipo="inner")["broadcast"] == "esquerda"


def test_full_outer_nunca_faz_broadcast():
    assert estrategia_join(1, 1, tipo="full")["estrategia"] == "sort_merge"


def test_empate_e_limite_desligado():
    assert estrategia_join(3, 3)["broadcast"] == "direita"
    assert estrategia_join(3, 3, limite_mb=-1)["estrategia"] == "sort_merge"
    with pytest.raises(ValueError):
        estrategia_join(1, 1, tipo="cross_apply")
