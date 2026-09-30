"""Exercício 09 (M9) — Dynamic Task Mapping sob um pool: quanto tempo leva.

Rode `pytest -q`. Detalhes no enunciado (exercicio-09.md).
"""

import heapq


def simular_pool(duracoes: list, slots: int, maiores_primeiro: bool = False) -> dict:
    """duracoes = minutos de cada instância mapeada, na ordem em que o mapeamento as cria.
    As instâncias entram na fila nessa ordem (ou da MAIOR para a menor, se maiores_primeiro, com empate
    pelo índice original); cada uma ocupa o primeiro slot que ficar livre (desempate: slot de menor número).
    Retorne {"inicio": [minuto de início de cada instância, na ordem ORIGINAL], "total": minuto em que a
    última termina}. slots < 1 -> ValueError. Lista vazia -> {"inicio": [], "total": 0}."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
