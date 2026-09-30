"""Exercício 05 (M23) — Saga orquestrada: compensar ou seguir em frente.

Rode `pytest -q`. Detalhes no enunciado (exercicio-05.md).
"""


def executar_saga(passos: list, pivo: str, resultados: dict) -> dict:
    """passos = [(nome, compensacao)] em ordem; pivo = nome do passo a partir do qual não se compensa
    (o próprio pivô já é irreversível). resultados = {passo: lista de sucesso/falha das tentativas,
    em ordem}; passo ausente = sempre sucesso.

    Regras:
      - passo ANTES do pivô: 1 tentativa. Se falhar, execute as compensações dos passos já concluídos,
        em ordem INVERSA, e pare com status "compensada".
      - pivô e passos depois dele: tente de novo até dar certo (consumindo a lista); se a lista acabar
        sem sucesso, pare com status "pendente" (vai para retry manual/fila), SEM compensar nada.
      - todos os passos ok -> "concluida".
    Retorne {"status": ..., "log": ["ok:passo", "falha:passo", "compensa:acao", ...]}.
    Pivô que não está nos passos -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
