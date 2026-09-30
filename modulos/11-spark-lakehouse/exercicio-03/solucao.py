"""Exercício 03 (M11) — groupBy com a semântica de nulos do Spark.

Rode `pytest -q`. Detalhes no enunciado (exercicio-03.md).
"""


def agregar(linhas: list, chave: str, coluna: str) -> list:
    """linhas = dicts (a chave ou a coluna podem faltar ou ser None). Para cada valor da chave (None é
    um grupo), retorne um dict {chave: valor, "linhas": count(*), "n": count(coluna), "soma": sum,
    "media": avg com 2 casas, "maximo": max}, com soma/média/máximo None se o grupo não tiver nenhum
    valor não nulo. Ordene pelos valores da chave com None por ÚLTIMO."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
