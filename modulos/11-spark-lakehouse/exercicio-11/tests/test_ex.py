import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import dividir_skew, particoes_skewed  # noqa: E402

# 12 partições depois de um groupBy por cliente; o cliente gigante caiu na partição 7
TAMANHOS = [110, 95, 120, 100, 105, 98, 130, 2_000, 115, 90, 102, 108]


def test_detecta_a_particao_gigante():
    assert particoes_skewed(TAMANHOS) == [7]


def test_precisa_passar_nos_dois_criterios():
    pequenas = [10, 10, 10, 200]          # 20x a mediana, mas abaixo de 256 MB: não vale dividir
    assert particoes_skewed(pequenas) == []
    assert particoes_skewed(pequenas, limiar_mb=100) == [3]


def test_dividir():
    r = dividir_skew(TAMANHOS)
    assert r["maior_antes"] == 2_000 and r["maior_depois"] == 130
    assert len(r["particoes"]) == 27 and r["particoes"][7:23] == [125.0] * 16


def test_sem_skew_nada_muda_e_vazio():
    r = dividir_skew([100, 110, 120])
    assert r == {"particoes": [100, 110, 120], "maior_antes": 120, "maior_depois": 120}
    assert particoes_skewed([]) == []
