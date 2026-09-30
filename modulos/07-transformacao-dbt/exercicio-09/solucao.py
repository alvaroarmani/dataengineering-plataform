"""Exercício 09 (M7) — Merge incremental: dado atrasado, duplicata no lote e exclusão lógica.

Rode `pytest -q`. Detalhes no enunciado (exercicio-09.md).
"""


def merge_incremental(destino: list, lote: list, chave: str) -> list:
    """destino e lote = listas de dicts com `chave`, "updated_at" e, opcionalmente, "_deleted".
    1. Deduplique o lote por chave, ficando com o MAIOR updated_at (empate: o que aparece por último).
    2. Para cada registro do lote deduplicado:
         - chave nova: insere (se não for _deleted);
         - chave existente: aplica só se updated_at do lote >= o do destino (atrasado é ignorado);
           aplicar um _deleted = remover do destino.
    Retorne o destino final ordenado por `chave`, sem o campo "_deleted". Não altere as entradas."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
