"""Testes do Exercício 01 (M20). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import servico_cloud  # noqa: E402


def test_servico_cloud():
    assert servico_cloud(*('objeto',)) == 'object-storage'
    assert servico_cloud(*('funcao',)) == 'serverless'
    assert servico_cloud(*('container',)) == 'orquestracao'
    assert servico_cloud(*('vm',)) == 'computacao'
