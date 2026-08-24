"""Exercício 03 (M5) — Consultando uma dimensão SCD Tipo 2.

Preencha as duas queries e rode `pytest -q`.

Tabela no teste:
dim_cliente(sk, cliente_id, cidade, valido_de DATE, valido_ate DATE, corrente BOOLEAN)
- mesma chave natural (cliente_id) pode ter várias linhas/versões.
"""

# A) VISÃO ATUAL: (cliente_id, cidade) apenas das linhas correntes, ordenado por cliente_id.
CONSULTA_A = """
-- SEU CÓDIGO AQUI
"""

# B) POINT-IN-TIME: (cliente_id, cidade) vigente em 01/07/2024,
# usando o intervalo valido_de/valido_ate. Ordene por cliente_id.
# Dica: WHERE valido_de <= DATE '2024-07-01' AND DATE '2024-07-01' < valido_ate
CONSULTA_B = """
-- SEU CÓDIGO AQUI
"""
