"""Exercício 11 (M11) — Skew: detectar e dividir partições como o AQE.

Rode `pytest -q`. Detalhes no enunciado (exercicio-11.md).
"""

import math
from statistics import median


def particoes_skewed(tamanhos_mb: list, fator: float = 5, limiar_mb: float = 256) -> list:
    """Índices (ordenados) das partições com tamanho > fator * mediana E tamanho > limiar_mb.
    Lista vazia -> []."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def dividir_skew(tamanhos_mb: list, fator: float = 5, limiar_mb: float = 256, alvo_mb: float = 128) -> dict:
    """Divida cada partição skewed em ceil(tamanho / alvo_mb) pedaços iguais. Retorne
    {"particoes": nova lista de tamanhos (pedaços no lugar da original, com 1 casa),
     "maior_antes": max original, "maior_depois": max novo (1 casa)}."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
