"""Exercício 04 (M8) — Dedup de reentrega, em Python (espelho do Exercício 03).

Implemente a deduplicação "versão mais recente por chave" e rode `pytest -q`.

Entrada: linhas = lista de tuplas (id, valor, carregado_em), com carregado_em em 'AAAA-MM-DD'.
"""


def dedup(linhas):
    """Retorne a lista de (id, valor) da versão MAIS RECENTE (maior carregado_em) de cada id,
    ORDENADA por id.

    - carregado_em pode vir como 'AAAA-MM-DD' ou 'AAAA-MM-DDTHH:MM:SS' (ISO — compara como texto).
    - As linhas podem chegar FORA de ordem; empate de carregado_em -> vence a que vem por último na lista.
    - valor None é uma EXCLUSÃO LÓGICA (tombstone): se a versão mais recente é None, o id sai do resultado.
    - Não altere a lista de entrada."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
