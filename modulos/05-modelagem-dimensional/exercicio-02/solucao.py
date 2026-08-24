"""Exercício 02 (M5) — Surrogate keys: gerar a dimensão e fazer o lookup.

Preencha as duas queries e rode `pytest -q`.

Tabelas disponíveis no teste:
- stg_produto(codigo VARCHAR, categoria VARCHAR)   -- staging da origem (chave natural)
- dim_produto(sk_produto, codigo, categoria)        -- dimensão já com surrogate key
- stg_venda(venda_id INT, codigo_produto VARCHAR, valor DOUBLE)
"""

# A) Gere a DIMENSÃO com surrogate key a partir de stg_produto.
# Colunas: (sk_produto, codigo, categoria). Use ROW_NUMBER() OVER (ORDER BY codigo).
CONSULTA_A = """
-- SEU CÓDIGO AQUI
"""

# B) Surrogate key lookup: monte o fato (venda_id, sk_produto, valor) juntando
# stg_venda a dim_produto pela chave natural (codigo). Ordene por venda_id.
CONSULTA_B = """
-- SEU CÓDIGO AQUI
"""
