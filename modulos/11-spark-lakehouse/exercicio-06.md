# Exercício 06 — Contar shuffles de um pipeline (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-06/solucao.py`](exercicio-06/solucao.py): implemente **`n_shuffles`** — conte os ops wide na sequência.

```bash
cd modulos/11-spark-lakehouse/exercicio-06
pytest -q
```

## Dica
:::{dropdown} Dica
`sum(1 for op in ops if op in wide)`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def n_shuffles(ops):
    wide = {'groupBy','join','distinct','orderBy','repartition'}
    return sum(1 for op in ops if op in wide)
```
:::

---
**Revisado em:** 2026-08-29
