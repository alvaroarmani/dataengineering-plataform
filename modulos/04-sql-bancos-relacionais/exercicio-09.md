# Exercício 09 — Window functions (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (usa DuckDB).

## Tarefas
Em [`exercicio-09/solucao.py`](exercicio-09/solucao.py):
- **`CONSULTA_A`** — (id, rn) com ROW_NUMBER por valor desc, ordenado por rn.
- **`CONSULTA_B`** — (id, acum) soma acumulada por ordem de id.

```bash
cd modulos/04-sql-bancos-relacionais/exercicio-09
pytest -q
```

> **Armadilhas nos testes:** além da base do enunciado, as mesmas queries rodam numa base com casos de borda. EMPATE de valor (id 3 e id 5 valem 80) — o ROW_NUMBER desempata pelo menor id.

## Dicas progressivas
:::{dropdown} Dica 1
`ROW_NUMBER() OVER (ORDER BY valor DESC)`.
:::
:::{dropdown} Dica 2
`SUM(valor) OVER (ORDER BY id)`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
-- CONSULTA_A
SELECT id, ROW_NUMBER() OVER (ORDER BY valor DESC, id) AS rn FROM itens ORDER BY rn

-- CONSULTA_B
SELECT id, SUM(valor) OVER (ORDER BY id) AS acum FROM itens ORDER BY id
```

**A armadilha do empate:** com dois itens de valor 80, `ROW_NUMBER() OVER (ORDER BY valor DESC)` sozinho é não determinístico; `ORDER BY valor DESC, id` fixa a ordem. Na soma acumulada, repare que o item de valor 0 repete o acumulado anterior.
:::

---
**Revisado em:** 2026-09-30
