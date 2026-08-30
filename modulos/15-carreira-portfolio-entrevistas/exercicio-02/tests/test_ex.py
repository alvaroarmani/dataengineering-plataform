"""Testes do Exercício 02 (M15). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import projetos_prontos  # noqa: E402


def test_projetos_prontos():
    assert projetos_prontos(*([{'nome': 'etl', 'tem_readme': True, 'tem_teste': True, 'versionado': True}, {'nome': 'scratch', 'tem_readme': False, 'tem_teste': True, 'versionado': True}],)) == ['etl']
    assert projetos_prontos(*([{'nome': 'x', 'tem_readme': True, 'tem_teste': False, 'versionado': True}],)) == []
