import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import passos_reconstruidos, tempo_de_build  # noqa: E402

RUIM = [{"instr": "FROM python:3.12-slim", "seg": 5},
        {"instr": "COPY . /app", "copia": ["."], "seg": 2},
        {"instr": "RUN pip install -r requirements.txt", "seg": 180},
        {"instr": "CMD python etl.py", "seg": 0}]
BOM = [{"instr": "FROM python:3.12-slim", "seg": 5},
       {"instr": "COPY requirements.txt /app/", "copia": ["requirements.txt"], "seg": 1},
       {"instr": "RUN pip install -r requirements.txt", "seg": 180},
       {"instr": "COPY src/ /app/src/", "copia": ["src/"], "seg": 1},
       {"instr": "CMD python src/etl.py", "seg": 0}]


def test_mudar_codigo_na_ordem_ruim_reinstala_tudo():
    alt = {"arquivos": ["src/etl.py"]}
    assert passos_reconstruidos(RUIM, alt) == [1, 2, 3]
    assert tempo_de_build(RUIM, alt) == 182


def test_mudar_codigo_na_ordem_boa_usa_o_cache():
    alt = {"arquivos": ["src/etl.py"]}
    assert passos_reconstruidos(BOM, alt) == [3, 4]
    assert tempo_de_build(BOM, alt) == 1


def test_mudar_dependencias_reinstala_nas_duas():
    alt = {"arquivos": ["requirements.txt"]}
    assert tempo_de_build(BOM, alt) == 182 and tempo_de_build(RUIM, alt) == 182


def test_mudar_a_imagem_base_refaz_tudo():
    assert passos_reconstruidos(BOM, {"instrucoes": [0]}) == [0, 1, 2, 3, 4]


def test_arquivo_que_nenhum_copy_inclui():
    assert passos_reconstruidos(BOM, {"arquivos": ["README.md"]}) == []
