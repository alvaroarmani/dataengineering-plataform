"""Exercício 04 (M5) — Analisando o star schema do Olist.

Preencha as duas queries e rode `pytest -q`.

Star schema (grão = 1 item de pedido):
- fato_item_pedido(sk_cliente, sk_produto, price, freight)
- dim_cliente(sk_cliente, customer_id, estado)
- dim_produto(sk_produto, product_id, categoria)
"""

# A) TICKET MÉDIO por categoria: colunas (categoria, ticket_medio) = AVG(price),
# ordenado do maior para o menor. Junte a fato com dim_produto.
CONSULTA_A = """
-- SEU CÓDIGO AQUI
"""

# B) RECEITA TOTAL por estado do cliente: colunas (estado, receita) = SUM(price + freight),
# ordenado do maior para o menor. Junte a fato com dim_cliente.
CONSULTA_B = """
-- SEU CÓDIGO AQUI
"""
