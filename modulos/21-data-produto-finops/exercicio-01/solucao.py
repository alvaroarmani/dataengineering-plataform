"""Exercício 01 (M21) — Custo pay-per-scan com mínimo por tabela.

Rode `pytest -q`. Detalhes no enunciado (exercicio-01.md).
"""

import math

MIB = 2 ** 20
TIB = 2 ** 40
MINIMO_POR_TABELA = 10 * MIB


def bytes_cobrados(bytes_por_tabela: list) -> int:
    """Uma consulta lê várias tabelas; bytes_por_tabela = bytes lidos em cada uma.
    Cada tabela é arredondada PARA CIMA ao MiB inteiro e cobrada no mínimo MINIMO_POR_TABELA
    (mesmo que tenha lido 0 byte). Retorne o total cobrado. Valor negativo -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def custo_mensal(consultas: list, preco_por_tib: float, gratis_tib: float = 1.0) -> float:
    """consultas = lista de consultas do mês (cada uma é uma lista de bytes por tabela).
    Custo = max(0, TiB cobrados - gratis_tib) * preco_por_tib, com 2 casas."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
