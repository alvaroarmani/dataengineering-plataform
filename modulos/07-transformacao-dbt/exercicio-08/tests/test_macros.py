"""Testes do Exercício 08 (M7). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import centavos_para_reais, surrogate_key  # noqa: E402


def test_centavos_para_reais():
    assert centavos_para_reais(12345) == 123.45
    assert centavos_para_reais(100) == 1.0
    assert centavos_para_reais(0) == 0.0


def test_surrogate_key_deterministica():
    assert surrogate_key(["p1", "2025"]) == surrogate_key(["p1", "2025"])


def test_surrogate_key_distingue():
    assert surrogate_key(["p1"]) != surrogate_key(["p2"])
    assert surrogate_key(["p1", "2025"]) != surrogate_key(["p1", "2024"])


def test_surrogate_key_e_string():
    sk = surrogate_key(["a", "b"])
    assert isinstance(sk, str) and len(sk) > 0
