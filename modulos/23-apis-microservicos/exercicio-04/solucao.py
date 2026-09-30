"""Exercício 04 (M23) — Política de retry: quem tentar de novo e quanto esperar.

Rode `pytest -q`. Detalhes no enunciado (exercicio-04.md).
"""


RETENTAVEIS = {429, 500, 502, 503, 504}


def espera(tentativa: int, base: float, teto: float) -> float:
    """Backoff exponencial: min(teto, base * 2 ** (tentativa - 1)); tentativa começa em 1."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def executar_com_retry(respostas: list, base: float, teto: float, max_tentativas: int) -> dict:
    """respostas = o que o servidor responde a cada chamada, em ordem: (status, retry_after ou None).
    Faça chamadas consumindo a lista:
      - 2xx -> sucesso, pare;
      - status fora de RETENTAVEIS (ex.: 400, 401, 404) -> falha definitiva, pare sem esperar;
      - retentável -> se ainda há tentativas, espere retry_after (se veio, limitado ao teto) ou
        espera(n, base, teto), e tente de novo; sem tentativas -> esgotado.
    Retorne {"resultado": "sucesso"|"falha_definitiva"|"esgotado", "tentativas": n, "esperas": [...]}."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
