"""Exercício 03 (M10) — Compose: depends_on com condição e tempo até o stack ficar pronto.

Rode `pytest -q`. Detalhes no enunciado (exercicio-03.md).
"""


def subir_stack(servicos: dict) -> dict:
    """servicos = {nome: {"inicio_seg": s, "health_seg": h ou None, "depende": {outro: condicao}}}
    condicao: "service_started" (basta o outro ter iniciado) ou "service_healthy" (o outro precisa estar
    saudável; exige que ele tenha health_seg). Um serviço COMEÇA a subir quando todas as condições valem
    (instante 0 se não depende de nada), fica "iniciado" inicio_seg depois e "saudável" health_seg depois
    de iniciado (sem healthcheck, saudável = iniciado).
    Retorne {"iniciado": {nome: t}, "saudavel": {nome: t}, "pronto_em": max saudável}.
    Dependência inexistente, service_healthy sem healthcheck ou ciclo -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
