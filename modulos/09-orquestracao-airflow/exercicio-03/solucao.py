"""Exercício 03 (M9) — XCom: dependências, e o limite do que se passa entre tasks.

Rode `pytest -q`. Detalhes no enunciado (exercicio-03.md).
"""

import json


def executar(tasks: list, limite_bytes: int = 1024) -> dict:
    """tasks = [(nome, [upstreams], func)] numa ordem em que cada upstream já apareceu antes.
    Cada func recebe um dict {upstream: xcom} SÓ com os seus upstreams e devolve o seu XCom.
    O XCom é serializado com json.dumps: se passar de `limite_bytes` bytes (len da string em UTF-8),
    levante ValueError dizendo qual task estourou. Upstream que ainda não rodou -> KeyError.
    Retorne {nome: xcom} de todas as tasks."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
