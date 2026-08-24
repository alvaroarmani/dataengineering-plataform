# Exercício 02 — Surrogate keys: gerar e usar (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (usa DuckDB).

Duas tarefas: **gerar** a surrogate key de uma dimensão e fazer o **surrogate key lookup**
ao carregar o fato.

## Tabelas
- `stg_produto(codigo, categoria)` — staging da origem, com a **chave natural** (`codigo`).
- `dim_produto(sk_produto, codigo, categoria)` — a dimensão já com surrogate key (para o item B).
- `stg_venda(venda_id, codigo_produto, valor)` — vendas com a chave natural.

## Tarefas
Em [`exercicio-02/solucao.py`](exercicio-02/solucao.py):

- **`CONSULTA_A`** — gere a **dimensão** `(sk_produto, codigo, categoria)` a partir de
  `stg_produto`, usando `ROW_NUMBER() OVER (ORDER BY codigo)` como surrogate key.
- **`CONSULTA_B`** — **surrogate key lookup**: monte o fato `(venda_id, sk_produto, valor)`
  juntando `stg_venda` a `dim_produto` pela chave natural (`codigo`), ordenado por `venda_id`.

```bash
cd modulos/05-modelagem-dimensional/exercicio-02
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — gerar a surrogate key
`SELECT ROW_NUMBER() OVER (ORDER BY codigo) AS sk_produto, codigo, categoria FROM stg_produto`.
:::
:::{dropdown} Dica 2 — o lookup
Junte pela **chave natural**: `stg_venda v JOIN dim_produto d ON v.codigo_produto = d.codigo`,
e selecione `v.venda_id, d.sk_produto, v.valor`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
-- CONSULTA_A: dimensão com surrogate key (inteiro sequencial, sem significado)
SELECT ROW_NUMBER() OVER (ORDER BY codigo) AS sk_produto, codigo, categoria
FROM stg_produto;

-- CONSULTA_B: surrogate key lookup — troca a chave natural pela surrogate
SELECT v.venda_id, d.sk_produto, v.valor
FROM stg_venda v
JOIN dim_produto d ON v.codigo_produto = d.codigo
ORDER BY v.venda_id;
```
A dimensão guarda **surrogate + natural**; o fato guarda só a **surrogate** (nunca 'P-100').
O *lookup* — JOIN pela chave natural para obter o `sk` — é exatamente o que o ETL faz ao
carregar cada tabela fato num Data Warehouse.
:::

---
**Revisado em:** 2026-08-23
