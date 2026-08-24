"""Exercício 01 (M6) — Camadas de um DW: do raw ao mart.

Preencha as duas queries e rode `pytest -q`.

Tabela no teste (dados CRUS, como chegam da fonte):
raw_pedidos(pedido_id INT, cliente VARCHAR, estado VARCHAR, valor DOUBLE)
- contém DUPLICATAS e o estado em caixa variada ('sp', 'SP', 'RJ'...).
"""

# A) CAMADA CORE: limpe o raw — remova duplicatas (DISTINCT) e padronize o estado (UPPER).
# Colunas (pedido_id, cliente, estado, valor), ordenado por pedido_id.
CONSULTA_A = """
-- SEU CÓDIGO AQUI
"""

# B) CAMADA MART: receita por estado (SUM(valor)), da maior para a menor.
# ATENÇÃO: agregue sobre os dados JÁ limpos (sem duplicatas), senão o total infla.
# Dica: use uma CTE com o SELECT DISTINCT do item A.
CONSULTA_B = """
-- SEU CÓDIGO AQUI
"""
