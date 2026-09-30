"""Exercício 05 (M19) — Roteamento de leitura: réplica ou líder?.

Rode `pytest -q`. Detalhes no enunciado (exercicio-05.md).
"""


def escolher_no_de_leitura(offset_lider: int, replicas: dict, lag_max: int, ultima_escrita_cliente: int = 0) -> str:
    """replicas = {nome: offset aplicado}. Lag de uma réplica = offset_lider - offset dela.
    Uma réplica é elegível se lag <= lag_max E offset >= ultima_escrita_cliente (read-your-writes).
    Retorne a elegível de MENOR lag (empate: menor nome); se nenhuma servir, "lider".
    Réplica à frente do líder (offset maior) é inconsistente -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
