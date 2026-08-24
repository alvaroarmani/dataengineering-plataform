"""Exercício 02 (M6) — Consultas que aproveitam colunar e particionamento.

Preencha as duas queries e rode `pytest -q`.

Tabela no teste (particionada logicamente por ano):
fato_vendas(ano INT, mes INT, categoria VARCHAR, valor DOUBLE)

Boas práticas: leia só as colunas necessárias e filtre pela coluna de partição (ano).
"""

# A) PRUNING: receita por categoria APENAS de 2025 (WHERE ano = 2025),
# colunas (categoria, receita) = SUM(valor), da maior para a menor.
CONSULTA_A = """
-- SEU CÓDIGO AQUI
"""

# B) FILTRO POR RANGE de partição: receita por ano considerando só ano >= 2024,
# colunas (ano, receita) = SUM(valor), ordenado por ano crescente.
CONSULTA_B = """
-- SEU CÓDIGO AQUI
"""
