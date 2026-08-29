"""Exercício 05 (M6) — Consultas cost-aware (leia só o necessário, filtre a partição).

Preencha as duas queries e rode `pytest -q`.

Tabela (particionada logicamente por ano):
fato(ano INT, mes INT, categoria VARCHAR, price INT, descricao VARCHAR)
- `descricao` é a coluna "gorda" — NÃO a selecione: cost-aware = ler só o necessário.
"""

# A) Receita por categoria em 2025 (só as colunas necessárias + filtro de partição):
# colunas (categoria, receita) = SUM(price), da maior para a menor.
CONSULTA_A = """
-- SEU CÓDIGO AQUI
"""

# B) O mês de MAIOR receita em 2025: colunas (mes, receita), apenas 1 linha (a maior).
CONSULTA_B = """
-- SEU CÓDIGO AQUI
"""
