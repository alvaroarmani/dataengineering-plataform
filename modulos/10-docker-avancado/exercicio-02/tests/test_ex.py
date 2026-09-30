import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import no_contexto, tamanho_do_contexto  # noqa: E402

ARQUIVOS = [".env", ".git/HEAD", "Dockerfile", "README.md", "requirements.txt", "src/etl.py",
            "src/__pycache__/etl.cpython-312.pyc", "src/utils/__pycache__/io.cpython-312.pyc",
            "data/raw_2gb.csv", "data/amostra.csv", "logs/run.log", "debug.log"]
REGRAS = ["# segredos e lixo", ".env", ".git/", "**/__pycache__", "*.log", "logs/",
          "", "data/", "!data/amostra.csv"]


def test_contexto_filtrado():
    assert no_contexto(ARQUIVOS, REGRAS) == ["Dockerfile", "README.md", "data/amostra.csv",
                                            "requirements.txt", "src/etl.py"]


def test_ultima_regra_vence():
    assert no_contexto(["data/amostra.csv"], ["!data/amostra.csv", "data/"]) == []


def test_sem_regras_vai_tudo():
    assert no_contexto(["a", "b/c"], []) == ["a", "b/c"]


def test_tamanho():
    tamanhos = {".env": 200, "data/raw_2gb.csv": 2_000_000_000, "data/amostra.csv": 50_000, "src/etl.py": 3_000}
    assert tamanho_do_contexto(tamanhos, []) == 2_000_053_200
    assert tamanho_do_contexto(tamanhos, REGRAS) == 53_000
