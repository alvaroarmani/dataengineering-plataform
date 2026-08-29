"""Exercício 04 (M7) — Consultando o star no navegador (espelho do mart dbt em DuckDB).

Mesma ideia do Exercício 03 (dbt real), aqui auto-corrigível. Preencha e rode `pytest -q`.

Tabelas (staging já limpo):
- stg_itens(item_id INT, produto_id VARCHAR, price DOUBLE)
- stg_produtos(produto_id VARCHAR, categoria VARCHAR)
"""

# A) Receita por categoria (join stg_itens + stg_produtos por produto_id):
# colunas (categoria, receita) = SUM(price), da maior para a menor.
CONSULTA_A = """
-- SEU CÓDIGO AQUI
"""

# B) Ticket médio por categoria: colunas (categoria, ticket_medio) = AVG(price),
# da maior para a menor.
CONSULTA_B = """
-- SEU CÓDIGO AQUI
"""
