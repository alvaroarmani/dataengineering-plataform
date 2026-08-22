"""Testes do Exercício 06 (M3). Faça todos passarem: pytest -q"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solucao import validar_registro  # noqa: E402


def test_valido():
    assert validar_registro({"id": 1, "valor": 10, "estado": "SP"}) == []


def test_todos_os_erros_em_ordem():
    assert validar_registro({"valor": -5, "estado": "XX"}) == [
        "id ausente",
        "valor negativo",
        "estado inválido",
    ]


def test_valor_ausente():
    assert validar_registro({"id": 1, "estado": "RJ"}) == ["valor ausente"]


def test_valor_ausente_nao_marca_negativo():
    # sem 'valor', não deve aparecer "valor negativo"
    assert validar_registro({"id": 1}) == ["valor ausente"]


def test_estado_opcional():
    # sem 'estado', nenhuma regra de estado dispara
    assert validar_registro({"id": 1, "valor": 0}) == []


def test_valor_zero_e_valido():
    assert validar_registro({"id": 2, "valor": 0, "estado": "MG"}) == []
