"""Exercício 05 (M3) — Achatar JSON de uma API.

Implemente `achatar_pedidos` e rode `pytest -q` nesta pasta até tudo passar.
"""


def achatar_pedidos(payload):
    """Recebe {"pedidos": [ {"id", "cliente": {"nome"}, "itens": [{"valor"}, ...]}, ... ]}.

    Retorna uma lista de dicts planos, um por pedido, na ordem de entrada, com:
      - id: o id do pedido
      - cliente: o nome do cliente (cliente.nome)
      - total: soma dos itens[].valor (0.0 se não houver itens)
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError
