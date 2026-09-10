"""Testes do Exercicio 01 (M23). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import status_http  # noqa: E402


def test_status_http():
    assert status_http(*('ok',)) == 200
    assert status_http(*('criado',)) == 201
    assert status_http(*('nao_encontrado',)) == 404
    assert status_http(*('boom',)) == 500
