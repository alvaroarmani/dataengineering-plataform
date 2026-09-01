"""Testes do Exercicio 04 (M2). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import arquivos_staged  # noqa: E402


def test_arquivos_staged():
    assert arquivos_staged(*({'a.py': 'staged', 'b.py': 'unstaged', 'c.py': 'staged'},)) == ['a.py', 'c.py']
    assert arquivos_staged(*({'x': 'untracked'},)) == []
