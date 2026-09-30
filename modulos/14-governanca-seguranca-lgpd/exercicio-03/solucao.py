"""Exercício 03 (M14) — Mascaramento por tipo de dado.

Rode `pytest -q`. Detalhes no enunciado (exercicio-03.md).
"""

import re


def mascarar(valor, tipo: str):
    """Tipos:
      "email"    -> 1º caractere da parte local + "***@" + domínio   ("ana@x.com" -> "a***@x.com");
                    sem exatamente um "@" ou com parte local/domínio vazio -> "***"
      "cpf"      -> "***.DDD.DDD-**" com os dígitos do meio (aceita "12345678909" ou "123.456.789-09");
                    se não tiver exatamente 11 dígitos -> "***"
      "telefone" -> troca por "*" todos os dígitos, menos os 4 últimos, preservando os outros caracteres
                    ("(11) 98765-4321" -> "(**) *****-4321"); menos de 4 dígitos -> "***"
    valor None -> None. Tipo desconhecido -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
