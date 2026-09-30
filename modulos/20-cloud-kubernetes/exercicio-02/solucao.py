"""Exercício 02 (M20) — Quantas réplicas? Capacidade que sobrevive à perda de uma zona.

Rode `pytest -q`. Detalhes no enunciado (exercicio-02.md).
"""

import math


def planejar_replicas(carga_pico: float, capacidade_pod: float, utilizacao_alvo: float = 0.7,
                      zonas: int = 1, tolerar_perda_zona: bool = False) -> dict:
    """Réplicas espalhadas IGUALMENTE entre as zonas (mesmo número por zona).
      necessarias = ceil(carga_pico / (capacidade_pod * utilizacao_alvo)), no mínimo 1
      sem tolerância: por_zona = ceil(necessarias / zonas)
      com tolerância: as zonas - 1 restantes precisam somar `necessarias`:
                      por_zona = ceil(necessarias / (zonas - 1))   (exige zonas >= 2)
    Retorne {"por_zona": n, "total": n * zonas, "utilizacao_normal": carga / (total * capacidade), 2 casas}.
    utilizacao_alvo fora de (0, 1], capacidade <= 0 ou tolerância com 1 zona -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
