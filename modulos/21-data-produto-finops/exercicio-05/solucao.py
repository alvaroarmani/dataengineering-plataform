"""Exercício 05 (M21) — SLO e orçamento de erro com incidentes sobrepostos.

Rode `pytest -q`. Detalhes no enunciado (exercicio-05.md).
"""

from datetime import datetime


def minutos_indisponiveis(incidentes: list) -> float:
    """incidentes = [(inicio, fim)] em ISO ('AAAA-MM-DD HH:MM'). Retorne os minutos da UNIÃO dos
    intervalos (sobreposições contam uma vez). fim < inicio -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def orcamento_de_erro(slo_pct: float, janela_dias: int, incidentes: list) -> dict:
    """permitido = (1 - slo_pct/100) * janela_dias * 1440 minutos.
    Retorne {"permitido_min", "consumido_min", "restante_min" (1 casa cada), "queimado_pct" (2 casas),
             "cumpre": consumido <= permitido}."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
