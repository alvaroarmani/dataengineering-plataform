"""Exercício 13 (M4) — Qual índice o banco consegue usar? (regra do prefixo em B-Tree composto).

Rode `pytest -q`.

Um índice B-Tree composto é uma lista ORDENADA de colunas, ex.: ["estado", "cidade", "data"].
Os filtros do WHERE são um dict coluna -> operador, ex.: {"estado": "=", "data": ">="}.

Operadores:
    "="                                         -> igualdade
    "<", ">", "<=", ">=", "between", "like_prefixo"   -> faixa  (like_prefixo = LIKE 'abc%')
    "like_sufixo", "funcao", "!="               -> não aproveitam índice (LIKE '%abc', UPPER(col), <>)
"""

FAIXA = {"<", ">", "<=", ">=", "between", "like_prefixo"}
NAO_INDEXAVEL = {"like_sufixo", "funcao", "!="}


def colunas_usadas(indice: list, filtros: dict) -> int:
    """Quantas colunas do índice (a partir da PRIMEIRA) o filtro consegue usar para navegar na árvore.

    Percorra o índice na ordem:
      - coluna com "="            -> conta e CONTINUA para a próxima;
      - coluna com operador de faixa -> conta e PARA (depois de uma faixa, a ordem se perde);
      - coluna ausente do filtro ou com operador não indexável -> PARA sem contar.
    Operador desconhecido -> ValueError.
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def melhor_indice(indices: dict, filtros: dict):
    """indices = {nome: [colunas...]}. Retorne o nome do índice que usa MAIS colunas.
    Empate: o índice com MENOS colunas (mais barato de ler); persistindo, o nome em ordem alfabética.
    Se nenhum índice usa ao menos 1 coluna, retorne None (o banco fará full scan)."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def evita_ordenacao(indice: list, filtros: dict, order_by: list) -> bool:
    """O índice entrega as linhas JÁ na ordem de `order_by` (dispensando um SORT)?

    Sim se existir uma posição j tal que:
      - todas as colunas indice[:j] estão no filtro com "=" (fixadas), e
      - indice[j : j + len(order_by)] == order_by.
    order_by vazio -> True.
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError
