"""Exercício 01 (M14) — Análise de impacto: quem avisar antes da mudança.

Rode `pytest -q`. Detalhes no enunciado (exercicio-01.md).
"""

from collections import deque


def analise_de_impacto(lineage: dict, tabela, donos: dict) -> dict:
    """lineage = {ativo: [ativos que o CONSOMEM]}; donos = {ativo: dono ou None}.
    Retorne:
      {"impactados": [ordenados, sem a própria tabela],
       "por_distancia": {1: [...], 2: [...], ...},     # menor distância de cada impactado, listas ordenadas
       "notificar": [donos distintos dos impactados, ordenados, sem None/""],
       "sem_dono": [impactados sem dono cadastrado, ordenados]}
    Deve terminar mesmo com ciclos. Tabela fora do lineage -> KeyError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
