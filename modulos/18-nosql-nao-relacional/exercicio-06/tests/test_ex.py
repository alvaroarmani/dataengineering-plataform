import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import escrever, ler  # noqa: E402


def _cluster():
    return [{"versao": 1, "valor": "v1"} for _ in range(3)]


def test_w2_r2_sempre_le_o_mais_novo():
    reps = escrever(_cluster(), 2, "v2", 2)            # grava nas réplicas 0 e 1
    assert ler(reps, 2) == "v2"
    assert ler(list(reversed(reps)), 2) == "v2"        # mesmo consultando a réplica atrasada primeiro


def test_w1_r1_pode_ler_dado_velho():
    reps = escrever(_cluster(), 1, "v2", 2)
    assert ler(reps, 1) == "v2"
    assert ler(list(reversed(reps)), 1) == "v1"        # R + W = 2, não > 3: leitura velha


def test_w1_r3_tambem_e_consistente():
    reps = escrever(_cluster(), 1, "v2", 2)
    assert ler(list(reversed(reps)), 3) == "v2"


def test_replica_fora_do_ar():
    reps = _cluster()
    reps[0] = None
    reps = escrever(reps, 2, "v2", 2)                  # grava nas réplicas 1 e 2
    assert reps[0] is None and ler(reps, 2) == "v2"


def test_sem_quorum_a_operacao_e_recusada():
    reps = [None, None, {"versao": 1, "valor": "v1"}]
    with pytest.raises(ValueError):
        escrever(reps, 2, "v2", 2)
    with pytest.raises(ValueError):
        ler(reps, 2)
    assert ler(reps, 1) == "v1"


def test_nao_altera_a_entrada():
    reps = _cluster()
    escrever(reps, 3, "v9", 9)
    assert reps == _cluster()
