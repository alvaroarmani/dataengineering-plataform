"""Testes do Exercício 06 (M15). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import undercurrents_faltando  # noqa: E402


def test_undercurrents_faltando():
    assert undercurrents_faltando(*(['qualidade', 'custo'],)) == ['idempotencia', 'observabilidade', 'seguranca']
    assert undercurrents_faltando(*(['qualidade', 'seguranca', 'observabilidade', 'custo', 'idempotencia'],)) == []
