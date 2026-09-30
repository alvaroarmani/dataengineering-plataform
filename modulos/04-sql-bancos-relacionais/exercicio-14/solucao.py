"""Exercício 14 (M4) — Poda por estatísticas (zone maps) com vários filtros.

Rode `pytest -q`. Detalhes no enunciado (exercicio-14.md).
"""


def blocos_lidos(blocos: list, filtros: dict) -> list:
    """blocos = [{coluna: (min, max) ou None (sem estatística)}]; filtros = {coluna: (lo, hi)} com lo/hi
    inclusivos e None = sem limite. Um bloco é lido se, para TODOS os filtros, o intervalo do bloco
    se sobrepõe à faixa (coluna sem estatística no bloco -> não dá para podar). Retorne os índices.
    Faixa com lo > hi -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def fracao_podada(blocos: list, filtros: dict) -> float:
    """Fração (2 casas) de blocos que NÃO precisam ser lidos. Sem blocos -> 0.0."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
