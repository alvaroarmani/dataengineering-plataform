"""Exercício 01 (M19) — Sharding por módulo: o custo de crescer.

Rode `pytest -q`. Detalhes no enunciado (exercicio-01.md).
"""

import zlib


def shard(chave: str, n: int) -> int:
    """zlib.crc32(chave em UTF-8) % n. n < 1 -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def fracao_realocada(chaves: list, n_antes: int, n_depois: int) -> float:
    """Fração (4 casas) das chaves cujo shard muda ao passar de n_antes para n_depois nós."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def armazenamento_por_no(dados_gb: float, fator: int, n_nos: int) -> float:
    """GB por nó (2 casas) com `fator` réplicas de cada dado, espalhadas por igual.
    Cada réplica de um dado precisa ficar num nó DIFERENTE: fator > n_nos -> ValueError.
    fator < 1 ou n_nos < 1 -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
