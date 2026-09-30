"""Exercício 09 (M8) — Aplicar um changelog de CDC: ordem, idempotência e anomalias.

Rode `pytest -q`. Detalhes no enunciado (exercicio-09.md).
"""


def aplicar_cdc(estado: dict, eventos: list) -> dict:
    """estado = {"tabela": {chave: valor}, "ultimo_lsn": int}.
    eventos = [{"lsn": int, "op": "I"|"U"|"D", "chave": ..., "valor": ...}] em qualquer ordem, com repetições.
    Aplique em ordem de LSN, pulando lsn <= ultimo_lsn (já aplicado) e LSN repetido no próprio lote.
      I: insere (se a chave já existir: sobrescreve e registra anomalia "I_existente")
      U: atualiza (se não existir: insere e registra "U_inexistente")
      D: remove (se não existir: registra "D_inexistente")
    op desconhecida -> ValueError. Não altere a entrada.
    Retorne {"tabela", "ultimo_lsn", "aplicados": n, "ignorados": n, "anomalias": [(lsn, tipo)]}."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
