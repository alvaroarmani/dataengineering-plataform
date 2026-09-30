"""Exercício 02 (M17) — Batch x streaming: medindo a latência de verdade.

Rode `pytest -q`. Detalhes no enunciado (exercicio-02.md).
"""

import math


def latencias_batch(eventos_min: list, intervalo_min: int, duracao_job_min: float) -> list:
    """eventos_min = instantes dos eventos, em minutos desde meia-noite.
    O job roda nos instantes múltiplos de `intervalo_min` (0, 60, 120, ...) e processa os eventos com
    instante ESTRITAMENTE menor que o de início do job; o dado fica disponível no fim do job.
    Latência de um evento = (início do primeiro job que o pega + duracao_job_min) - instante do evento."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def latencias_streaming(eventos_min: list, atraso_seg: float) -> list:
    """No streaming, cada evento fica disponível `atraso_seg` segundos depois; devolva em minutos."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def percentil(valores: list, p: float) -> float:
    """Percentil p (0-100) pelo método do "rank mais próximo": ordene; posição = ceil(p/100 * n),
    mínimo 1; retorne o valor nessa posição (1-indexada), com 2 casas. Lista vazia -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
