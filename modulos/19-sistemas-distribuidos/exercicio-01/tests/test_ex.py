import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
CHAVES = [f"cliente-{i}" for i in range(2000)]
from solucao import armazenamento_por_no, fracao_realocada, shard  # noqa: E402


def test_shard_estavel():
    assert shard("cliente-0", 4) == 3
    assert shard("cliente-1", 4) == 1
    assert all(0 <= shard(c, 7) < 7 for c in CHAVES)


@pytest.mark.parametrize("antes, depois, esperado", [
    (4, 5, 0.81),       # +1 nó: 81% dos dados se mudam
    (10, 11, 0.9055),
    (4, 8, 0.5),        # dobrar é o "menos pior" com módulo
    (4, 4, 0.0),
])
def test_fracao_realocada(antes, depois, esperado):
    assert fracao_realocada(CHAVES, antes, depois) == esperado


def test_armazenamento():
    assert armazenamento_por_no(900, 3, 6) == 450.0
    assert armazenamento_por_no(100, 1, 3) == 33.33
    with pytest.raises(ValueError):
        armazenamento_por_no(100, 3, 2)          # 3 cópias em 2 nós: duas no mesmo nó
    with pytest.raises(ValueError):
        shard("x", 0)


def test_lista_vazia():
    assert fracao_realocada([], 3, 4) == 0.0
