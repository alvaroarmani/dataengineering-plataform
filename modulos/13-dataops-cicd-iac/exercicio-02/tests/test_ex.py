"""Testes do Exercício 02 (M13). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import ambiente_do_branch  # noqa: E402


def test_ambiente_do_branch():
    assert ambiente_do_branch(*('main',)) == 'prod'
    assert ambiente_do_branch(*('develop',)) == 'staging'
    assert ambiente_do_branch(*('feature/x',)) == 'dev'
    assert ambiente_do_branch(*('hotfix',)) == 'nenhum'
