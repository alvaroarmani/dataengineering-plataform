"""Testes do Exercício 07 (M8). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import valida_registro  # noqa: E402

SCHEMA = {"id": int, "nome": str, "valor": float}


def test_registro_valido():
    assert valida_registro({"id": 1, "nome": "ana", "valor": 10.0}, SCHEMA) == []


def test_campo_faltando():
    assert valida_registro({"id": 1, "nome": "ana"}, SCHEMA) == ["valor"]


def test_tipo_errado():
    assert valida_registro({"id": "x", "nome": "ana", "valor": 10.0}, SCHEMA) == ["id"]


def test_varios_problemas_ordenados():
    # id ausente, valor com tipo errado -> ['id', 'valor'] ordenado
    assert valida_registro({"nome": "ana", "valor": "caro"}, SCHEMA) == ["id", "valor"]
