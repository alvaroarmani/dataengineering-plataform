"""Exercício 01 (M17) — Roteamento de eventos com padrões de tópico e DLQ.

Rode `pytest -q`. Detalhes no enunciado (exercicio-01.md).
"""


def casa(padrao: str, tipo: str) -> bool:
    """Tipos e padrões são segmentos separados por ponto ("pagamento.aprovado").
    "*" casa exatamente um segmento; "#" casa zero ou mais segmentos; o resto, igualdade."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def entregar(eventos: list, assinaturas: dict) -> dict:
    """eventos = [(id, tipo)]; assinaturas = {consumidor: [padroes]}.
    Retorne {consumidor: [ids na ordem dos eventos]} para TODO consumidor (lista vazia se nada casou)
    e a chave "DLQ" com os ids que nenhum consumidor recebeu. Um consumidor recebe cada evento no
    máximo uma vez, mesmo que vários padrões dele casem."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
