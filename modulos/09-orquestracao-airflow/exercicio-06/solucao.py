"""Exercício 06 (M9) — Carga idempotente de um dia, em Python (espelho do Exercício 05).

Reprocessar um dia deve SUBSTITUIR (overwrite da partição), não acumular. Implemente e rode
`pytest -q`.
"""


def carregar_dia(fato, dia, batch):
    """`fato` = lista de (data, id, valor); `batch` = lista de (id, valor) do `dia`.
    Retorne o novo `fato`: sem as linhas antigas de `dia`, com as do `batch` (marcadas com `dia`),
    ORDENADO por (data, id). Outros dias permanecem."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
