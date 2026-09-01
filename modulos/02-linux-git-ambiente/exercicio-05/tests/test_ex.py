"""Testes do Exercicio 05 (M2). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import tipo_docker  # noqa: E402


def test_tipo_docker():
    assert tipo_docker(*('molde',)) == 'imagem'
    assert tipo_docker(*('instancia',)) == 'container'
    assert tipo_docker(*('dados_persistentes',)) == 'volume'
    assert tipo_docker(*('x',)) == 'desconhecido'
