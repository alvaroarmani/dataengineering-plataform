"""Exercício 01 (M18) — Do relacional ao documento: desnormalizar e pagar o preço.

Rode `pytest -q`.

Entrada relacional (listas de dicts, como viriam de um SELECT):
    clientes = [{"id": 1, "nome": "Ana", "cidade": "Recife"}, ...]
    pedidos  = [{"id": 10, "cliente_id": 1, "data": "2026-03-01"}, ...]
    itens    = [{"pedido_id": 10, "produto": "livro", "qtd": 2, "preco": 39.9}, ...]
"""


def montar_documentos(clientes: list, pedidos: list, itens: list) -> list:
    """Monte UM documento por pedido (a consulta principal é "mostrar o pedido"), ordenados por _id:

        {"_id": 10, "data": "2026-03-01",
         "cliente": {"id": 1, "nome": "Ana", "cidade": "Recife"},     # cópia EMBUTIDA
         "itens": [{"produto": "livro", "qtd": 2, "preco": 39.9}],    # na ordem de `itens`
         "total": 79.8}                                               # soma qtd*preco, 2 casas

    - Pedido sem itens -> "itens": [] e "total": 0.0.
    - Pedido de cliente inexistente, ou item de pedido inexistente (órfão) -> ValueError.
    - Não compartilhe objetos entre documentos: cada documento tem a SUA cópia do cliente.
    """
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def pedidos_do_cliente(docs: list, cliente_id: int) -> list:
    """Lista dos _id dos pedidos do cliente, em ordem crescente."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError


def atualizar_cidade(docs: list, cliente_id: int, nova_cidade: str) -> int:
    """O cliente mudou de cidade. Atualize TODAS as cópias embutidas (altere `docs` no lugar) e
    retorne quantos documentos foram modificados — o custo de escrita da desnormalização.
    Documentos em que a cidade já era `nova_cidade` não contam como modificados."""
    # SEU CÓDIGO AQUI
    raise NotImplementedError
