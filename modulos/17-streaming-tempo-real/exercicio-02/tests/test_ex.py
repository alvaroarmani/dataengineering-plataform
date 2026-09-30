import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import latencias_batch, latencias_streaming, percentil  # noqa: E402

# instantes de 20 eventos ao longo de um dia (minutos desde 00:00)
EVENTOS = [3, 17, 58, 61, 119, 125, 180, 239, 250, 299, 301, 359, 480, 541, 600, 719, 720, 1000, 1319, 1439]


def test_latencia_individual():
    assert latencias_batch([3, 58, 60], intervalo_min=60, duracao_job_min=10) == [67, 12, 70]


def test_percentil_rank_mais_proximo():
    assert percentil([5, 1, 3, 2, 4], 50) == 3
    assert percentil([5, 1, 3, 2, 4], 95) == 5
    assert percentil([7], 0) == 7
    with pytest.raises(ValueError):
        percentil([], 50)


def test_batch_horario_p50_e_p95():
    lat = latencias_batch(EVENTOS, 60, 10)
    assert (percentil(lat, 50), percentil(lat, 95)) == (53, 70)


def test_batch_de_15_min_e_streaming():
    lat15 = latencias_batch(EVENTOS, 15, 3)
    assert (percentil(lat15, 50), percentil(lat15, 95)) == (8, 18)
    st = latencias_streaming(EVENTOS, atraso_seg=5)
    assert percentil(st, 95) == 0.08


def test_evento_no_corte_espera_o_ciclo_inteiro():
    # evento exatamente às 60: o job das 60 só pega eventos < 60, então ele vai no das 120
    assert latencias_batch([60], 60, 0) == [60]
