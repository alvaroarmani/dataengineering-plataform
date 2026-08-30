"""Testes do Exercício 04 (M12). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import valores_invalidos  # noqa: E402


def test_valores_invalidos():
    assert valores_invalidos(*(['pago', 'cancelado', 'x', 'pago'], ['pago', 'cancelado', 'enviado'])) == ['x']
