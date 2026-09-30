"""Exercício 03 (M13) — Workflow com dependências: quem roda, quem é pulado.

Rode `pytest -q`. Detalhes no enunciado (exercicio-03.md).
"""


def executar_workflow(jobs: dict, resultados: dict) -> dict:
    """jobs = {job: [jobs de que depende (needs)]}; resultados = {job: True/False} = o que o job
    faria SE rodasse (sucesso ou falha).

    Simule a execução: um job roda só depois das dependências; se alguma dependência terminou em
    "failure" ou "skipped", ele fica "skipped"; senão, fica "success" ou "failure" conforme `resultados`.
    Retorne {"jobs": {job: status} (ordem alfabética), "conclusao": "failure" se algum job falhou,
    senão "success"}. Dependência inexistente ou ciclo -> ValueError.
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError
