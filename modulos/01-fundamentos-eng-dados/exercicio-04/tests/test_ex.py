"""Testes do Exercicio 04 (M1). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import arquitetura_recomendada  # noqa: E402


def test_arquitetura_recomendada():
    assert arquitetura_recomendada(*('sql_estruturado',)) == 'data-warehouse'
    assert arquitetura_recomendada(*('dados_brutos',)) == 'data-lake'
    assert arquitetura_recomendada(*('ambos',)) == 'lakehouse'
