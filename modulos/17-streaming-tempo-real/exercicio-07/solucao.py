"""Exercício 07 (M17) — Particionamento por chave no Kafka (TRACK REAL · Kafka na bancada).

Implemente a preparação das mensagens. O grader produz e consome de um tópico REAL na bancada
(profile kafka) e verifica que a garantia de ordem por partição vale. Ver enunciado.
"""


def preparar_mensagens(eventos: list) -> list:
    """`eventos` é uma lista de dicts com 'cliente_id' e 'acao'. Retorne uma lista de tuplas
    **(chave, valor)** para produzir no Kafka, de modo que TODOS os eventos de um mesmo cliente
    caiam na MESMA partição (ordem por cliente) — e clientes diferentes se espalhem.

    A chave define a partição (hash da chave). O valor é a ação. Mantenha a ordem dos eventos.
    """
    # SEU CÓDIGO AQUI (dica: a chave deve identificar o cliente)
    raise NotImplementedError
