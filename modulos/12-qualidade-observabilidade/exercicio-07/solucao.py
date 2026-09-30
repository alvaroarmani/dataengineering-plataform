"""Exercício 07 (M12) — Roteamento de alertas por severidade.

Rode `pytest -q`. Detalhes no enunciado (exercicio-07.md).
"""


STATUS = {"pass", "warn", "fail"}


def decidir_alerta(resultados: list, criticos: set, limite_avisos: int = 3) -> dict:
    """resultados = lista de (check, status) em ordem cronológica; status em {"pass","warn","fail"}.
    O mesmo check pode aparecer mais de uma vez: vale o ÚLTIMO status (re-execução).

    Retorne {"acao": ..., "falhas": [checks com fail, ordenados], "avisos": [checks com warn, ordenados]}:
      "plantao"  se algum check CRÍTICO terminou em fail
      "canal"    senão, se houve algum fail OU pelo menos `limite_avisos` avisos
      "nada"     caso contrário
    Status desconhecido -> ValueError.
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError
