"""Exercício 04 (M15) — Case de modelagem: da tabela achatada ao star schema.

Rode `pytest -q`. Detalhes no enunciado (exercicio-04.md).
"""


def depende_de(linhas: list, chave: str) -> list:
    """Colunas (exceto a própria chave) que são FUNÇÃO da chave: para cada valor da chave, a coluna tem
    sempre o mesmo valor. Retorne ordenadas. Coluna que, em algum valor da chave, varia -> não depende."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def propor_star(linhas: list, chaves: list) -> dict:
    """Para cada chave candidata, dimensão "dim_<chave sem _id>" = [chave] + colunas que dependem dela.
    Uma coluna que depende de mais de uma chave vai para a dimensão da PRIMEIRA chave da lista.
    O fato "fato" = chaves + colunas que não foram para nenhuma dimensão (ordenadas).
    Retorne {"fato": [...], "dim_...": [...], ...}."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
