"""Testes do Exercício 04 (M6). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import bytes_varridos, custo_usd  # noqa: E402

BPC = {"a": 10, "b": 20, "c": 30}


def test_bytes_projecao():
    # lê a e c de 2 partições: (10+30)*2 = 80
    assert bytes_varridos(["a", "c"], 2, BPC) == 80


def test_bytes_todas_colunas_uma_particao():
    assert bytes_varridos(["a", "b", "c"], 1, BPC) == 60


def test_bytes_uma_coluna_muitas_particoes():
    assert bytes_varridos(["b"], 5, BPC) == 100


def test_custo_1tb():
    assert custo_usd(1_000_000_000_000) == 6.25


def test_custo_fracao_com_preco():
    assert custo_usd(200_000_000_000, preco_por_tb=6.25) == 1.25
