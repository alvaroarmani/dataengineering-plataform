"""Exercício 01 (M5) — Consultando um star schema.

Preencha as duas queries e rode `pytest -q`.
Tabelas: fato_vendas(venda_id, cliente_id, produto_id, quantidade, valor),
dim_cliente(cliente_id, nome, cidade), dim_produto(produto_id, categoria).
"""

# Receita por categoria (fato + dim_produto): colunas (categoria, receita), receita DESC.
CONSULTA_A = """
-- SEU CÓDIGO AQUI
"""

# Receita por cliente (fato + dim_cliente): colunas (nome, receita), receita DESC.
CONSULTA_B = """
-- SEU CÓDIGO AQUI
"""
