"""Testes do Exercício 02 (M12). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import valida_contrato  # noqa: E402


def test_valida_contrato():
    assert valida_contrato(*({'id': 'int', 'nome': 'str'}, {'id': 1, 'nome': 'a'})) == ['id', 'nome']
    assert valida_contrato(*({'id': 'int', 'nome': 'str'}, {'id': 'x'})) == ['id']
