"""Exercício 08 (M12) — Faixa esperada aprendida do histórico (IQR).

Rode `pytest -q`. Detalhes no enunciado (exercicio-08.md).
"""

from statistics import quantiles


def faixa_iqr(historico: list, k: float = 1.5) -> tuple:
    """(limite_inferior, limite_superior) = (Q1 - k*IQR, Q3 + k*IQR), com 2 casas, onde Q1 e Q3 vêm de
    statistics.quantiles(historico, n=4, method="inclusive"). Menos de 4 pontos -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def pontos_anomalos(serie: list, janela: int, k: float = 1.5) -> list:
    """Para cada índice i >= janela, compare serie[i] com a faixa_iqr das `janela` observações
    ANTERIORES (serie[i-janela:i]). Retorne os índices fora da faixa (limites inclusivos = normal)."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
