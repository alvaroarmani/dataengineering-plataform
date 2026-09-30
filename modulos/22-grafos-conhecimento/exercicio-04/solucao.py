"""Exercício 04 (M22) — Recomendação: pessoas que você talvez conheça.

Rode `pytest -q`. Detalhes no enunciado (exercicio-04.md).
"""


def amigos_em_comum(grafo: dict, a, b) -> list:
    """Vizinhos em comum de a e b, ordenados. Nó inexistente -> KeyError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def recomendar(grafo: dict, pessoa, top_n: int = 3) -> list:
    """Candidatos = amigos de amigos que NÃO são a própria pessoa nem já são amigos dela.
    Retorne até `top_n` pares (candidato, qtd_amigos_em_comum), ordenados por qtd desc e nome asc.
    Pessoa inexistente -> KeyError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
