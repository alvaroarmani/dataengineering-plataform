"""Exercício 06 (M13) — Resumo do plano e detecção de drift.

Rode `pytest -q`. Detalhes no enunciado (exercicio-06.md).
"""


def resumo_plano(plano: dict) -> str:
    """plano no formato do exercício 05 ({"criar", "atualizar", "substituir", "destruir"}).
    Retorne "Plan: A to add, C to change, D to destroy." — substituição conta em add E em destroy.
    Plano sem mudanças -> "No changes."."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def detectar_drift(estado: dict, real: dict) -> dict:
    """estado = o que o Terraform acha que existe; real = o que existe na nuvem ({nome: {atributos}}).
    Retorne {"alterados": {nome: [atributos divergentes, ordenados]},
             "nao_gerenciados": [existem na nuvem mas não no estado],
             "sumidos": [no estado mas não existem mais]} (listas ordenadas)."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
