"""Exercício 07 (M18) — Índice invertido com posições e busca por frase.

Rode `pytest -q`. Detalhes no enunciado (exercicio-07.md).
"""

import re
import unicodedata


def analisar(texto: str, stopwords: set) -> list:
    """Tokens do texto: sem acento, minúsculos, separados por qualquer caractere não alfanumérico,
    SEM as stopwords. A posição de cada token é a sua ordem na lista ANTES de remover stopwords —
    retorne pares (posicao, token)."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def indexar(docs: list, stopwords: set) -> dict:
    """docs = [(doc_id, texto)]. Retorne {termo: {doc_id: [posicoes]}} (posições em ordem)."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def buscar_frase(indice: dict, frase: str, stopwords: set) -> list:
    """doc_ids (ordenados) em que os termos da frase aparecem na MESMA sequência de posições relativas
    (respeitando os buracos deixados pelas stopwords). Frase vazia após análise -> []."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
