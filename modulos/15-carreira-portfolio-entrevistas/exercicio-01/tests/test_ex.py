"""Testes do Exercício 01 (M15). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import secoes_faltando  # noqa: E402


def test_secoes_faltando():
    assert secoes_faltando(*(['o que', 'como rodar'],)) == ['arquitetura', 'o que aprendi', 'por que']
    assert secoes_faltando(*(['o que', 'por que', 'arquitetura', 'como rodar', 'o que aprendi'],)) == []
