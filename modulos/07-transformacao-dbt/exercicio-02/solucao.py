"""Exercício 02 (M7) — Staging + mart no navegador (espelho do dbt em DuckDB).

Mesma lógica do Exercício 01 (dbt real), aqui auto-corrigível no navegador. Preencha as
duas queries e rode `pytest -q`.

Tabela crua: raw_pedidos(id VARCHAR, cliente VARCHAR, uf VARCHAR, valor_str VARCHAR)
"""

# A) STAGING: limpe raw_pedidos -> (pedido_id INT, cliente, estado=UPPER(uf), valor=DOUBLE),
# ordenado por pedido_id.
CONSULTA_A = """
-- SEU CÓDIGO AQUI
"""

# B) MART: receita por estado = SUM(valor) a partir da lógica de staging,
# colunas (estado, receita), da maior para a menor.
CONSULTA_B = """
-- SEU CÓDIGO AQUI
"""
