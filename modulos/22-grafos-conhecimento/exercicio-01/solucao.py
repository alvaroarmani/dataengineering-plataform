"""Exercício 01 (M22) — Da tabela de arestas à lista de adjacência.

Rode `pytest -q`. Detalhes no enunciado (exercicio-01.md).
"""


def construir_grafo(arestas: list, dirigido: bool = False) -> dict:
    """arestas = lista de pares (origem, destino). Retorne {no: [vizinhos ORDENADOS e sem repetição]}.

    - Não dirigido: a aresta (a, b) aparece em a E em b. Dirigido: só a -> b.
    - Todo nó que aparece em alguma aresta existe no grafo (mesmo sem vizinhos de saída).
    - Aresta repetida conta uma vez; laço (a, a) é ignorado — mas o nó passa a existir.
    - Par com None -> ValueError.
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def vizinhos(grafo: dict, no) -> list:
    """Vizinhos de `no`; nó inexistente -> KeyError com mensagem clara."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
