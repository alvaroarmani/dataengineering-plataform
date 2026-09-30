"""Exercício 06 (M9) — Backfill idempotente com overwrite por partição.

Rode `pytest -q`. Detalhes no enunciado (exercicio-06.md).
"""

from datetime import date, timedelta


def carregar_dia(fato: list, dia: str, lote: list) -> list:
    """fato = [(data, id, valor)]; lote = [(id, valor)] do `dia`. Retorne o novo fato: sem as linhas
    antigas de `dia`, com as do lote marcadas com `dia`, ORDENADO por (data, id). Id repetido no lote
    -> ValueError (a fonte veio duplicada)."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def backfill(fato: list, fonte: dict, inicio: str, fim: str) -> list:
    """Rode carregar_dia para cada dia de inicio a fim (inclusive), usando fonte.get(dia, []) — dia
    ausente na fonte ESVAZIA a partição. inicio > fim -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
