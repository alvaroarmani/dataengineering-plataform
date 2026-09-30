"""Exercício 04 (M21) — TCO: self-hosted x gerenciado e o mês de virada.

Rode `pytest -q`. Detalhes no enunciado (exercicio-04.md).
"""


def tco(opcao: dict, meses: int) -> float:
    """opcao = {"inicial", "mensal", "crescimento" (fração ao mês, composta), "horas_mes", "custo_hora"}.
    TCO = inicial + soma, para m = 1..meses, de  mensal * (1 + crescimento) ** (m - 1)  +  horas_mes * custo_hora.
    (Só a infraestrutura cresce; o custo de pessoas é constante.) 2 casas. meses < 0 -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def comparar(opcoes: dict, meses: int) -> dict:
    """{"tco": {nome: tco}, "mais_barata": nome} (empate: ordem alfabética)."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def mes_de_virada(a: dict, b: dict, max_meses: int = 120):
    """Primeiro mês m (1..max_meses) em que o TCO acumulado de `a` fica MENOR OU IGUAL ao de `b`,
    sendo que no mês 1 `a` era mais cara. Se `a` já é mais barata (ou igual) no mês 1, retorne 1.
    Se nunca virar no horizonte, retorne None."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
