"""Exercício 04 (M20) — HPA de verdade: tolerância, limites e várias métricas.

Rode `pytest -q`. Detalhes no enunciado (exercicio-04.md).
"""

import math


def hpa(atual: int, metricas: dict, min_replicas: int, max_replicas: int, tolerancia: float = 0.1) -> dict:
    """metricas = {nome: (valor_atual, alvo)}. Para cada métrica, razão = valor / alvo:
      se |razão - 1| <= tolerancia -> propõe manter `atual`; senão -> ceil(atual * razão).
    Desejado = maior proposta entre as métricas, limitado a [min_replicas, max_replicas].
    Retorne {"replicas": n, "motivo": nome da métrica que decidiu (a de maior proposta; empate:
    ordem alfabética) ou "limite_min"/"limite_max" se o limite mudou o valor}.
    Sem métricas, alvo <= 0 ou min > max -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
