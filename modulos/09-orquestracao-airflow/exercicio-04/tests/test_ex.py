import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import simular_sensor  # noqa: E402


def test_arquivo_chega_no_minuto_47():
    poke = simular_sensor(47, intervalo=5, timeout=120, modo="poke")
    resch = simular_sensor(47, intervalo=5, timeout=120, modo="reschedule")
    assert poke == {"sucesso": True, "pokes": 11, "minuto_fim": 50, "minutos_de_slot": 51}
    assert resch == {"sucesso": True, "pokes": 11, "minuto_fim": 50, "minutos_de_slot": 11}


def test_ja_disponivel():
    assert simular_sensor(0, 5, 60, "poke") == {"sucesso": True, "pokes": 1, "minuto_fim": 0, "minutos_de_slot": 1}


def test_timeout():
    r = simular_sensor(None, intervalo=10, timeout=60, modo="poke")
    assert r == {"sucesso": False, "pokes": 7, "minuto_fim": 60, "minutos_de_slot": 61}
    assert simular_sensor(200, 10, 60, "reschedule")["minutos_de_slot"] == 7


def test_duzentos_sensores_numa_manha():
    total_poke = 200 * simular_sensor(180, 5, 240, "poke")["minutos_de_slot"]
    total_resch = 200 * simular_sensor(180, 5, 240, "reschedule")["minutos_de_slot"]
    assert (total_poke, total_resch) == (36_200, 7_400)


def test_invalidos():
    with pytest.raises(ValueError):
        simular_sensor(10, 0, 60, "poke")
    with pytest.raises(ValueError):
        simular_sensor(10, 5, 60, "deferred")
