# Exercício 04 — withColumn: coluna derivada (imutável) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py): implemente **`com_receita`** — monte novos dicts com `{**r, 'receita': ...}` (DataFrames são imutáveis).

```bash
cd modulos/11-spark-lakehouse/exercicio-04
pytest -q
```

## Dica
:::{dropdown} Dica
Use dict unpacking para não mutar.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def com_receita(linhas):
    return [{**r, 'receita': r['preco'] * r['qtd']} for r in linhas]
```
:::

---
**Revisado em:** 2026-08-29
