import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import desfazer_rle, rle, taxa_compressao  # noqa: E402

ESTADOS = ["SP", "RJ", "SP", "MG", "SP", "RJ", "SP", "SP", "MG", "RJ", "SP", "RJ"] * 50   # 600 valores


def test_rle_basico():
    assert rle(["SP", "SP", "RJ", "SP"]) == [("SP", 2), ("RJ", 1), ("SP", 1)]
    assert rle([]) == []


def test_ida_e_volta_sem_perda():
    assert desfazer_rle(rle(ESTADOS)) == ESTADOS
    with pytest.raises(ValueError):
        desfazer_rle([("SP", 0)])


def test_ordenar_muda_tudo():
    assert taxa_compressao(ESTADOS) == 1.09          # desordenado: quase nada
    assert taxa_compressao(sorted(ESTADOS)) == 200.0  # ordenado: 3 pares para 600 valores


def test_alta_cardinalidade_nao_comprime():
    ids = list(range(1000))
    assert taxa_compressao(ids) == 1.0
    assert taxa_compressao(sorted(ids)) == 1.0        # ordenar não ajuda: nada se repete


def test_vazio():
    assert taxa_compressao([]) == 1.0
