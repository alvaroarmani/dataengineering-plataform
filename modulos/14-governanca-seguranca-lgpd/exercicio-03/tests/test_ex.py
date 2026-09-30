import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solucao import mascarar  # noqa: E402


@pytest.mark.parametrize("valor, esperado", [
    ("ana@x.com", "a***@x.com"),
    ("bruno.silva@empresa.com.br", "b***@empresa.com.br"),
    ("  eva@y.io ", "e***@y.io"),
    ("sem-arroba.com", "***"),
    ("a@b@c.com", "***"),
    ("@dominio.com", "***"),
])
def test_email(valor, esperado):
    assert mascarar(valor, "email") == esperado


@pytest.mark.parametrize("valor, esperado", [
    ("123.456.789-09", "***.456.789-**"),
    ("12345678909", "***.456.789-**"),
    (12345678909, "***.456.789-**"),
    ("123.456.789", "***"),
])
def test_cpf(valor, esperado):
    assert mascarar(valor, "cpf") == esperado


@pytest.mark.parametrize("valor, esperado", [
    ("(11) 98765-4321", "(**) *****-4321"),
    ("+55 11 98765-4321", "+** ** *****-4321"),
    ("123", "***"),
])
def test_telefone(valor, esperado):
    assert mascarar(valor, "telefone") == esperado


def test_nulo_e_tipo_desconhecido():
    assert mascarar(None, "cpf") is None
    with pytest.raises(ValueError):
        mascarar("x", "rg")
