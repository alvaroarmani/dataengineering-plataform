"""Exercício 07 (M3) — Estatísticas em uma passada (streaming de verdade).

Rode `pytest -q`. Detalhes no enunciado (exercicio-07.md).
"""

import math


def agrega_stream(eventos) -> dict:
    """eventos = QUALQUER iterável de (chave, valor) — pode ser um generator que só dá para percorrer
    UMA vez. Retorne {chave: {"n", "soma", "min", "max", "media", "desvio"}} com média e desvio-padrão
    POPULACIONAL (4 casas), calculados pelo algoritmo de Welford:
        n += 1; delta = x - media; media += delta / n; m2 += delta * (x - media)
        desvio = sqrt(m2 / n)
    Valor None é ignorado (não conta em n)."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
