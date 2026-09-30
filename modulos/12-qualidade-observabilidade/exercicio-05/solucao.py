"""Exercício 05 (M12) — Freshness com SLA e aviso antecipado.

Rode `pytest -q`. Detalhes no enunciado (exercicio-05.md).
"""

from datetime import datetime


def status_freshness(ultima: str, agora: str, sla_horas: float, aviso_pct: float = 0.8) -> str:
    """Datas ISO ('AAAA-MM-DD HH:MM' ou com 'T'). atraso = agora - ultima, em horas.
      atraso > sla_horas                -> "violado"
      atraso > aviso_pct * sla_horas    -> "aviso"
      senão                             -> "ok"
    Última carga no FUTURO (relógio errado) -> ValueError.
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def relatorio(tabelas: dict, agora: str, sla_horas: float) -> dict:
    """tabelas = {nome: ultima_carga}. Retorne {"status": {nome: status}, "pior": nome}
    onde "pior" é a tabela com MAIOR atraso (empate: ordem alfabética). Sem tabelas -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
