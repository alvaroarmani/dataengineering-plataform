import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import arquivos_da_versao, removiveis_no_vacuum, versao_no_instante  # noqa: E402

LOG = [
    {"ts": 100, "add": ["p0.parquet", "p1.parquet"]},                       # v0: carga inicial
    {"ts": 200, "add": ["p2.parquet"]},                                       # v1: append
    {"ts": 300, "remove": ["p1.parquet"], "add": ["p1b.parquet"]},           # v2: MERGE reescreveu p1
    {"ts": 400, "remove": ["p0.parquet", "p1b.parquet", "p2.parquet"],
     "add": ["c0.parquet"]},                                                  # v3: OPTIMIZE compactou
]


def test_reproduzir_versoes():
    assert arquivos_da_versao(LOG, 0) == ["p0.parquet", "p1.parquet"]
    assert arquivos_da_versao(LOG, 2) == ["p0.parquet", "p1b.parquet", "p2.parquet"]
    assert arquivos_da_versao(LOG, 3) == ["c0.parquet"]


def test_time_travel_por_instante():
    assert versao_no_instante(LOG, 250) == 1
    assert versao_no_instante(LOG, 300) == 2
    assert versao_no_instante(LOG, 10_000) == 3
    with pytest.raises(ValueError):
        versao_no_instante(LOG, 50)


def test_vacuum_respeita_retencao():
    assert removiveis_no_vacuum(LOG, agora=450, retencao=100) == ["p1.parquet"]
    assert removiveis_no_vacuum(LOG, agora=600, retencao=100) == ["p0.parquet", "p1.parquet", "p1b.parquet", "p2.parquet"]


def test_versao_inexistente():
    with pytest.raises(ValueError):
        arquivos_da_versao(LOG, 7)
