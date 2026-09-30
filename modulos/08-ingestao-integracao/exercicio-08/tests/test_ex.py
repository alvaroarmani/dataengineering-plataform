import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import poll  # noqa: E402

LOG = [f"m{i}" for i in range(100, 110)]      # offsets 100..109 (0..99 já expiraram)


def test_leitura_normal_em_lotes():
    assert poll(LOG, 100, 103, max_msgs=4) == {"mensagens": ["m103", "m104", "m105", "m106"],
                                               "proximo_offset": 107, "perdidas": 0}
    assert poll(LOG, 100, 107, max_msgs=4) == {"mensagens": ["m107", "m108", "m109"],
                                               "proximo_offset": 110, "perdidas": 0}


def test_em_dia_nada_novo():
    assert poll(LOG, 100, 110) == {"mensagens": [], "proximo_offset": 110, "perdidas": 0}


def test_consumidor_atrasado_earliest():
    r = poll(LOG, 100, 95, max_msgs=3)
    assert r == {"mensagens": ["m100", "m101", "m102"], "proximo_offset": 103, "perdidas": 5}


def test_consumidor_atrasado_latest_perde_tudo_pendente():
    assert poll(LOG, 100, 95, reset="latest") == {"mensagens": [], "proximo_offset": 110, "perdidas": 15}


def test_none_exige_decisao_e_offset_invalido():
    with pytest.raises(ValueError):
        poll(LOG, 100, 95, reset="none")
    with pytest.raises(ValueError):
        poll(LOG, 100, 111)
    with pytest.raises(ValueError):
        poll(LOG, 100, 100, max_msgs=0)
