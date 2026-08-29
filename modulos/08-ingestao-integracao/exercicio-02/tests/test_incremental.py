"""Testes do Exercício 02 (M8). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import incremental, nova_marca  # noqa: E402

LINHAS = [(1, "2026-08-10"), (2, "2026-08-15"), (3, "2026-08-20")]


def test_incremental_seleciona_pos_marca():
    assert incremental(LINHAS, "2026-08-12") == [2, 3]


def test_incremental_estritamente_maior():
    # marca exatamente na data de bruno: não reinclui bruno
    assert incremental(LINHAS, "2026-08-15") == [3]


def test_incremental_vazio_quando_tudo_antigo():
    assert incremental(LINHAS, "2026-08-31") == []


def test_nova_marca():
    assert nova_marca(LINHAS) == "2026-08-20"


def test_nova_marca_vazio():
    assert nova_marca([]) is None
