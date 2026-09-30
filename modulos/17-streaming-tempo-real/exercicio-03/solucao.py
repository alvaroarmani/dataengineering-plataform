"""Exercício 03 (M17) — Particionamento por chave e ordem garantida.

Rode `pytest -q`. Detalhes no enunciado (exercicio-03.md).
"""

import zlib


def particao(chave: str, n: int) -> int:
    """zlib.crc32(chave em UTF-8) % n (o Kafka real usa murmur2; a ideia é a mesma)."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def produzir(mensagens: list, n: int) -> dict:
    """mensagens = [(chave ou None, valor)] na ordem de envio. Retorne {particao: [valores em ordem]}
    com TODAS as partições 0..n-1 (vazias inclusive). Com chave: particao(chave, n). Sem chave:
    round-robin entre as partições (a 1ª sem chave vai para a 0, a 2ª para a 1, ...)."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def chaves_remapeadas(chaves: list, n_antes: int, n_depois: int) -> list:
    """Chaves (ordenadas, sem repetição) cuja partição muda ao ir de n_antes para n_depois partições."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
