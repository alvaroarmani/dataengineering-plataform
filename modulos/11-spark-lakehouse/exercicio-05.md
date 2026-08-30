# Exercício 05 — Narrow vs wide (causa shuffle?) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-05/solucao.py`](exercicio-05/solucao.py): implemente **`causa_shuffle`** — wide = groupBy/join/distinct/orderBy/repartition; o resto é narrow.

```bash
cd modulos/11-spark-lakehouse/exercicio-05
pytest -q
```

## Dica
:::{dropdown} Dica
Compare com o conjunto de operações wide.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def causa_shuffle(op):
    wide = {'groupBy','join','distinct','orderBy','repartition'}
    return op in wide
```
:::

---
**Revisado em:** 2026-08-29
