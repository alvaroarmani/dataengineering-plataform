"""Exercício 06 (M7) — Os testes do dbt "por baixo" (Python).

Um teste dbt é uma query que busca VIOLAÇÕES (0 = passa). Implemente as duas checagens
que sustentam `relationships` e `unique`, e rode `pytest -q`.
"""


def orfaos(fato_produto_ids, dim_produto_ids):
    """relationships: retorne a lista ORDENADA e SEM repetição dos produto_id que aparecem
    no fato mas NÃO existem na dimensão (as violações de integridade referencial)."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def duplicados(valores):
    """unique: retorne a lista ORDENADA dos valores que aparecem MAIS DE UMA VEZ."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
