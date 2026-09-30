"""Exercício 05 (M22) — Centralidade: quem são os hubs da rede.

Rode `pytest -q`. Detalhes no enunciado (exercicio-05.md).
"""


def ranking_centralidade(grafo: dict, top_n: int = 3) -> list:
    """Para cada nó: (no, grau, grau_normalizado, alcance_2_saltos).
      grau_normalizado = grau / (n - 1), com 3 casas (n = nº de nós; rede de 1 nó -> 0.0)
      alcance_2_saltos = nós distintos a 1 ou 2 saltos, sem contar o próprio nó
    Ordene por grau desc, alcance desc, nome asc e retorne os `top_n` primeiros.
    Grafo vazio -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
