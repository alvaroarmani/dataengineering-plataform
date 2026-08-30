"""Testes do Exercício 04 (M11). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import com_receita  # noqa: E402


def test_com_receita():
    assert com_receita(*([{'preco': 10, 'qtd': 2}, {'preco': 5, 'qtd': 3}],)) == [{'preco': 10, 'qtd': 2, 'receita': 20}, {'preco': 5, 'qtd': 3, 'receita': 15}]
