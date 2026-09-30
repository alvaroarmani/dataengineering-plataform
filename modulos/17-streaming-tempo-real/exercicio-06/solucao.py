"""Exercício 06 (M17) — Exactly-once de efeito: offset, falha e reprocessamento.

Rode `pytest -q`. Detalhes no enunciado (exercicio-06.md).
"""

import copy


def processar(log: list, estado: dict, commit_a_cada: int, falha_apos=None, idempotente: bool = True) -> dict:
    """log = [(id, valor)] (o tópico; a posição na lista é o offset).
    estado = {"offset": próximo offset a ler (commitado), "saldo": número, "aplicados": set de ids}.

    Leia a partir de estado["offset"]. Para cada mensagem:
      - efeito: se idempotente e o id já está em "aplicados", ignore; senão some o valor no saldo e
        registre o id em "aplicados" (efeito e registro são atômicos);
      - depois de cada `commit_a_cada` mensagens processadas NESTA execução, commite
        (offset = posição seguinte à última processada).
      - se `falha_apos` = k, a execução "cai" logo depois de processar a k-ésima mensagem desta
        execução, ANTES de um eventual commit dela: devolva o estado nesse momento.
    Ao terminar o log sem falha, commite o que faltar. Não altere o estado de entrada."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
