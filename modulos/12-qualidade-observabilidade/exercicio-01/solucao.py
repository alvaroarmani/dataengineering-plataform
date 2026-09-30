"""Exercício 01 (M12) — Perfil de completude de um lote.

Rode `pytest -q`. Detalhes no enunciado (exercicio-01.md).
"""

import math


def perfil_completude(linhas: list, campos: list) -> dict:
    """Retorne {campo: fração de linhas com valor PRESENTE}, com 4 casas.

    Conta como AUSENTE: chave inexistente, None, float NaN e string vazia ou só com espaços.
    (0 e False são valores presentes!) Lote vazio -> ValueError.
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def campos_abaixo(perfil: dict, limiar: float) -> list:
    """Campos cuja completude é MENOR que o limiar, ordenados do pior para o melhor
    (empate: ordem alfabética)."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
