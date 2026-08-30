"""Testes do Exercício 05 (M14). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import classifica  # noqa: E402


def test_classifica():
    assert classifica(*('cpf',)) == 'pessoal'
    assert classifica(*('saude',)) == 'sensivel'
    assert classifica(*('valor',)) == 'comum'
