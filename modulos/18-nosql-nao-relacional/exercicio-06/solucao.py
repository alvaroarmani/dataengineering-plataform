"""Exercício 06 (M18) — Quóruns na prática: simular R + W > N.

Rode `pytest -q`. Detalhes no enunciado (exercicio-06.md).
"""

import copy


def escrever(replicas: list, w: int, valor, versao: int) -> list:
    """replicas = lista de estados, na ORDEM em que respondem: None (fora do ar) ou
    {"versao": int, "valor": ...}. Grave (versao, valor) nas W PRIMEIRAS réplicas disponíveis.
    Menos de W disponíveis -> ValueError (escrita NÃO confirmada; nada é gravado).
    Retorne a nova lista (não altere a entrada)."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def ler(replicas: list, r: int):
    """Consulte as R PRIMEIRAS réplicas disponíveis e retorne o valor de MAIOR versão entre elas.
    Menos de R disponíveis -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
