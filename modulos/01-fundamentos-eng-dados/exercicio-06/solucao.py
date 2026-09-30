"""Exercício 06 (M1) — Compressão por run-length: por que ordenar comprime.

Rode `pytest -q`. Detalhes no enunciado (exercicio-06.md).
"""


def rle(coluna: list) -> list:
    """Lista de pares (valor, repeticoes) para sequências CONSECUTIVAS de valores iguais."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def desfazer_rle(pares: list) -> list:
    """Reconstrói a coluna. Repetição < 1 -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def taxa_compressao(coluna: list) -> float:
    """len(coluna) / len(rle(coluna)), com 2 casas (1.0 = nada comprimiu). Coluna vazia -> 1.0."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
