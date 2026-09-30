import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import bytes_lidos, ganho  # noqa: E402

# 10 milhões de vendas; 3 colunas de negócio + 27 "outras" (8 bytes cada, pouco compressíveis)
FATO = {"linhas": 10_000_000, "colunas": {
    "estado": {"bytes": 2, "compressao": 20},       # 27 valores possíveis: comprime muito
    "data": {"bytes": 4, "compressao": 8},
    "valor": {"bytes": 8, "compressao": 2},
    **{f"col_{i}": {"bytes": 8, "compressao": 1.5} for i in range(27)},
}}


def test_por_linha_le_tudo():
    assert bytes_lidos(FATO, ["valor"], "linha") == 2_300_000_000


def test_colunar_le_so_o_necessario_e_comprimido():
    assert bytes_lidos(FATO, ["valor"], "coluna") == 40_000_000
    assert bytes_lidos(FATO, ["estado", "data", "valor"], "coluna") == 46_000_000


def test_ganho():
    assert ganho(FATO, ["estado", "data", "valor"]) == 50.0
    assert ganho(FATO, ["valor"]) == 57.5


def test_select_estrela_no_colunar_perde_a_vantagem():
    todas = list(FATO["colunas"])
    assert ganho(FATO, todas) == 1.5


def test_invalidos():
    with pytest.raises(ValueError):
        bytes_lidos(FATO, ["cliente"], "coluna")
    with pytest.raises(ValueError):
        bytes_lidos(FATO, ["valor"], "json")
