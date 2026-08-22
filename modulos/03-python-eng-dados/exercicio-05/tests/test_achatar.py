"""Testes do Exercício 05 (M3). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import achatar_pedidos  # noqa: E402


def test_um_pedido():
    payload = {"pedidos": [
        {"id": 1, "cliente": {"nome": "ana"}, "itens": [{"valor": 50}, {"valor": 30}]},
    ]}
    assert achatar_pedidos(payload) == [{"id": 1, "cliente": "ana", "total": 80.0}]


def test_varios_e_ordem():
    payload = {"pedidos": [
        {"id": 1, "cliente": {"nome": "ana"}, "itens": [{"valor": 50}, {"valor": 30}]},
        {"id": 2, "cliente": {"nome": "bruno"}, "itens": [{"valor": 1200}]},
        {"id": 3, "cliente": {"nome": "ana"}, "itens": [{"valor": 80}, {"valor": 20}]},
    ]}
    assert achatar_pedidos(payload) == [
        {"id": 1, "cliente": "ana", "total": 80.0},
        {"id": 2, "cliente": "bruno", "total": 1200.0},
        {"id": 3, "cliente": "ana", "total": 100.0},
    ]


def test_sem_itens():
    payload = {"pedidos": [{"id": 9, "cliente": {"nome": "caio"}, "itens": []}]}
    assert achatar_pedidos(payload) == [{"id": 9, "cliente": "caio", "total": 0.0}]


def test_vazio():
    assert achatar_pedidos({"pedidos": []}) == []
