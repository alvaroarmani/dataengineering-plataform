import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
CHAVES = [f"cliente-{i}" for i in range(2000)]
from collections import Counter

from solucao import construir_anel, fracao_realocada_anel, no_responsavel, replicas  # noqa: E402

NOS4 = ["n1", "n2", "n3", "n4"]
NOS5 = NOS4 + ["n5"]


def test_anel_ordenado_com_vnodes():
    anel = construir_anel(["a", "b"], vnodes=3)
    assert len(anel) == 6 and anel == sorted(anel)
    assert Counter(no for _, no in anel) == {"a": 3, "b": 3}


def test_responsavel_e_volta_no_anel():
    anel = [(100, "a"), (200, "b"), (300, "c")]
    assert no_responsavel(anel, "cliente-0") in {"a", "b", "c"}
    assert no_responsavel([(10, "x")], "qualquer") == "x"
    with pytest.raises(ValueError):
        no_responsavel([], "x")


def test_so_um_quinto_se_move_e_so_para_o_no_novo():
    assert fracao_realocada_anel(CHAVES, NOS4, NOS5, vnodes=50) == 0.202
    a, d = construir_anel(NOS4, 50), construir_anel(NOS5, 50)
    destinos = {no_responsavel(d, c) for c in CHAVES if no_responsavel(a, c) != no_responsavel(d, c)}
    assert destinos == {"n5"}


def test_vnodes_equilibram_a_carga():
    def maior_fatia(v):
        anel = construir_anel(NOS4, v)
        return max(Counter(no_responsavel(anel, c) for c in CHAVES).values())
    assert maior_fatia(1) == 1950        # sem vnodes: um nó fica com 97,5% das chaves
    assert maior_fatia(100) == 570       # com 100 vnodes: perto dos 500 ideais


def test_replicas_em_nos_distintos():
    anel = construir_anel(NOS4, vnodes=50)
    r = replicas(anel, "cliente-42", 3)
    assert len(r) == 3 and len(set(r)) == 3 and r[0] == no_responsavel(anel, "cliente-42")
    with pytest.raises(ValueError):
        replicas(anel, "cliente-42", 5)
