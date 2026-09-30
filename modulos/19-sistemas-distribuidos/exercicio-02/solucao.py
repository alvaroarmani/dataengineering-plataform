"""Exercício 02 (M19) — Hashing consistente com nós virtuais.

Rode `pytest -q`. Detalhes no enunciado (exercicio-02.md).
"""

import bisect
import zlib

ESPACO = 2 ** 32


def construir_anel(nos: list, vnodes: int = 1) -> list:
    """Lista ORDENADA de (posicao, no): cada nó ocupa `vnodes` posições, calculadas com
    zlib.crc32(f"{no}#{i}") para i = 0..vnodes-1."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def no_responsavel(anel: list, chave: str) -> str:
    """Primeiro nó com posição >= crc32(chave); se passar do fim, dá a volta (índice 0).
    Anel vazio -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def fracao_realocada_anel(chaves: list, nos_antes: list, nos_depois: list, vnodes: int = 1) -> float:
    """Fração (4 casas) das chaves cujo nó responsável muda."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def replicas(anel: list, chave: str, r: int) -> list:
    """Os r primeiros nós DISTINTOS a partir do responsável, no sentido horário (a "preference list").
    r maior que o número de nós distintos -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
