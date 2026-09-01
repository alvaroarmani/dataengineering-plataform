"""Testes do Exercicio 03 (M2). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import commit_valido  # noqa: E402


def test_commit_valido():
    assert commit_valido(*('feat: nova dag',)) == True
    assert commit_valido(*('fix(m2): typo',)) == True
    assert commit_valido(*('mudei umas coisas',)) == False
