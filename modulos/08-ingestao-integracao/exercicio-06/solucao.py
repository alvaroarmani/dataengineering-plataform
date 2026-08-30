"""Exercício 06 (M8) — Retry: reagir a falhas transitórias (rate limit 429, timeout).

Implemente o retry e rode `pytest -q`. (O backoff — esperar mais a cada tentativa — fica de
fora aqui para o teste ser rápido; o conceito está na teoria.)
"""


def com_retry(fn, tentativas=3):
    """Chame `fn()`. Se ela levantar exceção, tente de novo — até `tentativas` chamadas no
    total. Retorne o resultado no primeiro sucesso; se esgotar, RELANCE a última exceção."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
