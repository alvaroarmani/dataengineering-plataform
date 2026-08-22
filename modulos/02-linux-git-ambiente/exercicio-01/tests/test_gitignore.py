"""Testes do Exercício 01 (M2). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import arquivos_ignorados  # noqa: E402


ARQUIVOS = [".env", "app.py", "debug.log", "erro.log", "data/vendas.csv", "README.md"]


def test_nome_exato():
    assert arquivos_ignorados(ARQUIVOS, [".env"]) == [".env"]


def test_curinga_extensao():
    assert arquivos_ignorados(ARQUIVOS, ["*.log"]) == ["debug.log", "erro.log"]


def test_pasta_prefixo():
    assert arquivos_ignorados(ARQUIVOS, ["data/"]) == ["data/vendas.csv"]


def test_multiplos_padroes_e_ordem():
    assert arquivos_ignorados(ARQUIVOS, ["*.log", ".env", "data/"]) == [
        ".env",
        "debug.log",
        "erro.log",
        "data/vendas.csv",
    ]


def test_nada_casa():
    assert arquivos_ignorados(ARQUIVOS, ["*.tmp"]) == []
