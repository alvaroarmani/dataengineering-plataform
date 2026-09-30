"""Exercício 06 (M2) — Portas publicadas: parse e conflitos.

Rode `pytest -q`. Detalhes no enunciado (exercicio-06.md).
"""


def parse_porta(spec: str) -> dict:
    """Formatos: "C", "H:C", "IP:H:C", com sufixo opcional "/tcp" ou "/udp" (padrão tcp).
    Retorne {"ip": ip ou "0.0.0.0", "host": int ou None (só "C" = porta aleatória), "container": int,
    "protocolo": "tcp"|"udp"}. Porta fora de 1..65535, protocolo desconhecido ou formato inválido -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def conflitos(servicos: dict) -> list:
    """servicos = {servico: [specs]}. Dois mapeamentos conflitam se usam a MESMA porta de host e o mesmo
    protocolo, e os IPs colidem (iguais, ou algum deles é "0.0.0.0", que escuta em todos).
    Retorne a lista ORDENADA de (porta_host, protocolo, [servicos envolvidos ordenados]); portas
    aleatórias (host None) nunca conflitam."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
