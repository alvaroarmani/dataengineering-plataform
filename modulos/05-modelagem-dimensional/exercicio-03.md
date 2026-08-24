# Exercício 03 — Consultando uma dimensão SCD2 (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (usa DuckDB).

Duas consultas clássicas sobre uma dimensão **Slowly Changing Dimension Tipo 2**: a visão
atual e o *point-in-time*.

## Tabela
`dim_cliente(sk, cliente_id, cidade, valido_de, valido_ate, corrente)` — a mesma chave
natural (`cliente_id`) pode ter várias linhas, uma por versão.

## Tarefas
Em [`exercicio-03/solucao.py`](exercicio-03/solucao.py):

- **`CONSULTA_A`** — **visão atual**: `(cliente_id, cidade)` só das linhas correntes,
  ordenado por `cliente_id`.
- **`CONSULTA_B`** — **point-in-time**: `(cliente_id, cidade)` vigente em **01/07/2024**,
  usando o intervalo `valido_de`/`valido_ate`, ordenado por `cliente_id`.

```bash
cd modulos/05-modelagem-dimensional/exercicio-03
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — visão atual
A linha vigente hoje tem `corrente = TRUE`: `WHERE corrente`.
:::
:::{dropdown} Dica 2 — point-in-time
A versão vigente numa data está no intervalo:
`WHERE valido_de <= DATE '2024-07-01' AND DATE '2024-07-01' < valido_ate`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
-- CONSULTA_A: visão atual (a linha corrente de cada cliente)
SELECT cliente_id, cidade
FROM dim_cliente
WHERE corrente
ORDER BY cliente_id;

-- CONSULTA_B: point-in-time — a versão vigente em 01/07/2024
SELECT cliente_id, cidade
FROM dim_cliente
WHERE valido_de <= DATE '2024-07-01' AND DATE '2024-07-01' < valido_ate
ORDER BY cliente_id;
```
A flag `corrente` responde "como está hoje"; o intervalo `valido_de`/`valido_ate` responde
"como estava naquela data" — as duas formas de ler um SCD2. Repare que a comparação usa
`<` no fim (`data < valido_ate`) para não pegar duas versões na fronteira do intervalo.
:::

---
**Revisado em:** 2026-08-23
