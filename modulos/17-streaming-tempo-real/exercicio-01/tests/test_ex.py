"""Testes do Exercício 01 (M17). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import roteia  # noqa: E402


def test_roteia():
    assert roteia(*('pedido_criado', {'faturamento': ['pedido_criado'], 'antifraude': ['pedido_criado', 'pagamento'], 'estoque': ['pagamento']})) == ['antifraude', 'faturamento']
    assert roteia(*('pagamento', {'faturamento': ['pedido_criado'], 'antifraude': ['pedido_criado', 'pagamento'], 'estoque': ['pagamento']})) == ['antifraude', 'estoque']
