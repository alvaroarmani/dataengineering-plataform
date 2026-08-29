"""Exercício 02 (M8) — A lógica do incremental (marca d'água), em Python.

Implemente a seleção incremental e o avanço da marca d'água, e rode `pytest -q`.

Entrada: linhas = lista de tuplas (id, updated_at), com updated_at em 'AAAA-MM-DD'.
"""


def incremental(linhas, marca):
    """Retorne a lista ORDENADA de `id` cujas linhas têm updated_at ESTRITAMENTE maior
    que `marca` (as que precisam ser ingeridas)."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def nova_marca(linhas):
    """Retorne a maior updated_at (a nova marca d'água a persistir). Se vazio, retorne None."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
