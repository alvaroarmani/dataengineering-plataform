"""Exercício 06 (M11) — Stages e shuffles de um plano.

Rode `pytest -q`. Detalhes no enunciado (exercicio-06.md).
"""


NARROW = {"filter", "select", "withColumn", "map", "union"}
WIDE = {"groupBy", "distinct", "orderBy", "repartition"}


def analisar_plano(plano: list, limite_broadcast_mb: float = 10) -> dict:
    """plano = lista de passos: ("filter",), ("groupBy",), ... ou ("join", tamanho_do_outro_lado_mb).
    Um join é broadcast (narrow, sem shuffle) se o outro lado <= limite; senão, é um shuffle.
    "coalesce" é narrow (reduz partições sem shuffle).
    Retorne {"stages": 1 + shuffles, "shuffles": n, "broadcasts": n}. Passo desconhecido -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
