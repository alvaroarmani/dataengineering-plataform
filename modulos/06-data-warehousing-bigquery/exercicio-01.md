# Exercício 01 — Camadas de um DW: do raw ao mart (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (usa DuckDB).

Você recebe dados **crus** (com duplicatas e estado em caixa variada) e precisa produzir a
camada **core** (limpa) e um **mart** (agregado para consumo).

## Tabela
`raw_pedidos(pedido_id, cliente, estado, valor)` — dados como chegam da fonte, **com
duplicatas** e `estado` inconsistente ('sp', 'SP', 'RJ'...).

## Tarefas
Em [`exercicio-01/solucao.py`](exercicio-01/solucao.py):

- **`CONSULTA_A`** — **camada core**: remova duplicatas (`DISTINCT`) e padronize o estado
  (`UPPER`). Colunas `(pedido_id, cliente, estado, valor)`, ordenado por `pedido_id`.
- **`CONSULTA_B`** — **mart**: receita por estado (`SUM(valor)`), da maior para a menor,
  **sobre os dados já limpos** (senão a duplicata infla o total).

```bash
cd modulos/06-data-warehousing-bigquery/exercicio-01
pytest -q
```

> **Armadilhas nos testes:** além da base do enunciado, as mesmas queries rodam numa base com casos de borda. A mesma reentrega com o estado escrito de jeitos diferentes ('Sp', ' sp ') — só vira UMA linha se você padronizar com TRIM + UPPER ANTES de deduplicar.

## Dicas progressivas
:::{dropdown} Dica 1 — core
`SELECT DISTINCT pedido_id, cliente, UPPER(estado) AS estado, valor FROM raw_pedidos`.
:::
:::{dropdown} Dica 2 — mart sem inflar
Agregue sobre o core, não sobre o raw. Use uma CTE:
`WITH core AS (SELECT DISTINCT ...) SELECT estado, SUM(valor) ... FROM core GROUP BY estado`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
-- CONSULTA_A: camada core (limpa e padronizada)
SELECT DISTINCT pedido_id, cliente, UPPER(TRIM(estado)) AS estado, valor   -- padroniza, depois deduplica
FROM raw_pedidos
ORDER BY pedido_id;

-- CONSULTA_B: mart sobre o core (dedup evita inflar SP)
WITH core AS (
    SELECT DISTINCT pedido_id, cliente, UPPER(TRIM(estado)) AS estado, valor
    FROM raw_pedidos
)
SELECT estado, SUM(valor) AS receita
FROM core
GROUP BY estado
ORDER BY receita DESC;
```
A duplicata do pedido 1 mostra por que a camada **core** existe: se você agregar direto no
raw, SP viraria 280 em vez de 180. Limpar antes de consumir é o coração da arquitetura em camadas.

**A armadilha da ordem:** padronize **antes** de deduplicar. `DISTINCT` compara o texto exato — `'Sp'`, `' sp '` e `'SP'` são três valores diferentes até passarem por `UPPER(TRIM(...))`. Na camada core, limpeza vem sempre antes de dedup e de agregação.
:::

---
**Revisado em:** 2026-09-30
