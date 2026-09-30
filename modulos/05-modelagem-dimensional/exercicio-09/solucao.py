"""Exercício 09 (M5) — Fato de snapshot acumulado: lead times, pedidos em aberto e gargalo.

Rode `pytest -q`. Detalhes no enunciado (exercicio-09.md).
"""

from datetime import date

ETAPAS = ["criado", "pago", "enviado", "entregue"]


def snapshot_acumulado(pedidos: list, data_ref: str) -> list:
    """pedidos = [{"pedido_id", "criado", "pago"?, "enviado"?, "entregue"?}] (datas 'AAAA-MM-DD').
    Uma linha por pedido, ordenada por pedido_id:
      status          última etapa (na ordem de ETAPAS) que tem data
      dias_pago       criado -> pago;   dias_envio  pago -> enviado;   dias_entrega  enviado -> entregue
      dias_total      criado -> entregue
      (lead time é None se faltar qualquer uma das duas datas)
      dias_em_aberto  data_ref - criado, só para pedidos NÃO entregues (entregues: None)
      inconsistente   True se alguma data presente é ANTERIOR a uma data presente de etapa anterior
    Pedido sem "criado" -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def gargalo(snapshot: list) -> tuple:
    """Entre dias_pago, dias_envio e dias_entrega, a etapa de MAIOR média (ignorando None e linhas
    inconsistentes). Retorne (nome_da_coluna, media com 1 casa). Sem dados -> ValueError."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
