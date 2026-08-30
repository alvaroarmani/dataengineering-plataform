"""Testes do Exercício 03 (M11). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import receita_por_categoria  # noqa: E402


def test_receita_por_categoria():
    assert receita_por_categoria(*([{'categoria': 'A', 'preco': 10, 'qtd': 2}, {'categoria': 'B', 'preco': 5, 'qtd': 1}, {'categoria': 'A', 'preco': 3, 'qtd': 4}],)) == [('A', 32), ('B', 5)]
