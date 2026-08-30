"""Testes do Exercício 03 (M14). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import mascarar_email  # noqa: E402


def test_mascarar_email():
    assert mascarar_email(*('ana@x.com',)) == 'a***@x.com'
    assert mascarar_email(*('bruno@empresa.com.br',)) == 'b***@empresa.com.br'
