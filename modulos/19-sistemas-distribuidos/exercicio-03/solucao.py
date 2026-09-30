"""Exercício 03 (M19) — Partição de rede: quem pode continuar?.

Rode `pytest -q`. Detalhes no enunciado (exercicio-03.md).
"""


def falhas_toleradas(n: int) -> int:
    """Quantos nós podem cair com a maioria ainda viva: (n - 1) // 2. n < 1 -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def nos_para_tolerar(f: int) -> int:
    """Menor cluster que tolera f falhas: 2f + 1. f < 0 -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def lado_com_quorum(n_total: int, particoes: list):
    """particoes = lista de conjuntos de nós VIVOS e conectados entre si após a falha (nós mortos
    simplesmente não aparecem). Retorne o índice da partição com MAIORIA ESTRITA do cluster original
    (mais que n_total/2), ou None se nenhuma tiver. Nó repetido em duas partições -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
