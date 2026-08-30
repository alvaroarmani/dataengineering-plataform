"""Exercício 07 (M9) — Retries do Airflow (retries=N => N+1 tentativas).

Implemente a política de retry de uma task e rode `pytest -q`.
"""


def executar_com_retries(fn, retries):
    """Execute `fn()`. No Airflow, `retries=N` permite até N+1 TENTATIVAS (1 original + N).
    `fn` levanta exceção ao falhar. Retorne (sucesso, tentativas):
    - (True, k)  se passou na k-ésima tentativa;
    - (False, N+1) se falhou em todas."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
