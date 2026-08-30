"""Testes do Exercício 03 (M13). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import rodar_pipeline  # noqa: E402


def test_rodar_pipeline():
    assert rodar_pipeline(*([('lint', True), ('test', True), ('deploy', True)],)) == (True, None)
    assert rodar_pipeline(*([('lint', True), ('test', False), ('deploy', True)],)) == (False, 'test')
