"""Exercício 03 (M15) — SQL ao vivo: top N por grupo (window function).

Simula a prova de "SQL ao vivo" de entrevista. Preencha a query e rode `pytest -q`.
Tabela: vendas(produto_id, categoria, valor).
"""

# Top 2 produtos por RECEITA (soma de valor) em CADA categoria.
# Colunas de saída: (categoria, produto_id, receita).
# Ordene por categoria ASC, depois receita DESC. Desempate por produto_id ASC.
# Dica: agregue por (categoria, produto_id); rankeie com
#   ROW_NUMBER() OVER (PARTITION BY categoria ORDER BY SUM(valor) DESC, produto_id ASC)
# e filtre rn <= 2.
CONSULTA = """
-- SEU CÓDIGO AQUI
"""
