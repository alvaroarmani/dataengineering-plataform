"""Exercício 08 (M9) — Trigger rules: quem roda quando algo falha.

Rode `pytest -q`. Detalhes no enunciado (exercicio-08.md).
"""


FINAIS = {"success", "failed", "skipped", "upstream_failed"}


def estado_task(regra: str, upstreams: list):
    """Decide o que acontece com uma task dados os estados FINAIS das upstreams:
      all_success: roda se todas "success"; se alguma "failed"/"upstream_failed" -> "upstream_failed";
                   senão (alguma skipped) -> "skipped"
      all_done:    sempre roda
      one_failed:  roda se alguma "failed"/"upstream_failed"; senão -> "skipped"
      none_failed: roda se nenhuma "failed"/"upstream_failed"; senão -> "upstream_failed"
    Sem upstreams, sempre roda. Retorne "run" ou o estado final. Regra desconhecida -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def executar_dag(dag: dict, resultados: dict) -> dict:
    """dag = {task: {"upstream": [...], "regra": ...}} (sem ciclos); resultados = {task: True/False} =
    se a task teria sucesso ao rodar. Processe as tasks em ordem de dependência (desempate alfabético)
    e retorne {"estados": {task: estado final} em ordem alfabética,
               "run": "failed" se alguma task ficou "failed", senão "success"}. Ciclo -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
