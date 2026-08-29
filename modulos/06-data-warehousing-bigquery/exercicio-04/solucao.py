"""Exercício 04 (M6) — O modelo de custo do DW cloud (por bytes varridos).

Implemente as duas funções e rode `pytest -q`.
"""


def bytes_varridos(colunas_lidas, particoes_lidas, bytes_por_coluna):
    """Bytes que uma query varre no modelo colunar por partição.

    - colunas_lidas: lista de nomes de coluna que a query lê.
    - particoes_lidas: quantas partições a query lê (após o pruning).
    - bytes_por_coluna: dict {coluna: bytes por partição}.

    Retorne a soma dos bytes das colunas lidas, multiplicada pelas partições lidas.
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def custo_usd(bytes_varridos_total, preco_por_tb=6.25):
    """Custo em US$ dado o total de bytes varridos (1 TB = 1e12 bytes)."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
