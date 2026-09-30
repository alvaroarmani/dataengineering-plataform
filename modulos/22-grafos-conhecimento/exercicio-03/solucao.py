"""Exercício 03 (M22) — Caminho mais curto e vizinhança de k saltos (BFS).

Rode `pytest -q`. Detalhes no enunciado (exercicio-03.md).
"""

from collections import deque


def caminho_mais_curto(grafo: dict, origem, destino):
    """Lista de nós de `origem` até `destino` (inclusive) com o MENOR número de saltos.
    Explore os vizinhos em ordem alfabética: entre caminhos de mesmo tamanho, vence o primeiro
    encontrado assim. origem == destino -> [origem]; sem caminho -> None;
    origem ou destino fora do grafo -> KeyError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def ate_k_saltos(grafo: dict, origem, k: int) -> dict:
    """{no: distancia} para todo nó a no máximo k saltos (a origem com distância 0).
    k < 0 -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
