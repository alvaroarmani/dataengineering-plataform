"""Testes do Exercicio 09 (M5). Faca todos passarem: pytest -q"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import snapshot_acumulado  # noqa: E402


def test_snapshot_acumulado():
    assert snapshot_acumulado(*([{'pedido_id': 1, 'criado': '2026-01-01', 'pago': '2026-01-02', 'enviado': '2026-01-05', 'entregue': '2026-01-10'}, {'pedido_id': 2, 'criado': '2026-01-01', 'pago': '2026-01-03'}],)) == [{'pedido_id': 1, 'status': 'entregue', 'dias_pago': 1, 'dias_envio': 3, 'dias_entrega': 5, 'dias_total': 9}, {'pedido_id': 2, 'status': 'pago', 'dias_pago': 2, 'dias_envio': None, 'dias_entrega': None, 'dias_total': None}]
    assert snapshot_acumulado(*([{'pedido_id': 3, 'criado': '2026-02-01'}],)) == [{'pedido_id': 3, 'status': 'criado', 'dias_pago': None, 'dias_envio': None, 'dias_entrega': None, 'dias_total': None}]
