"""Testes do Exercício 04 (M18). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import chave_particao  # noqa: E402


def test_chave_particao():
    assert chave_particao(*({'pais': 'BR', 'ano': 2026, 'v': 1}, ['pais', 'ano'])) == ('BR', 2026)
    assert chave_particao(*({'id': 7}, ['id'])) == (7,)
