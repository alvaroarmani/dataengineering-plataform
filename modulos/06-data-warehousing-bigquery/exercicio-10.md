# Exercicio 10 - Layout fisico a partir do workload (nivel avancado)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro). Aplica a [teoria 05](teoria-05-otimizacao-consultas-avancada.md).

## Tarefa
Em [`exercicio-10/solucao.py`](exercicio-10/solucao.py): implemente **`layout_recomendado`** - consultas = lista de listas de colunas filtradas em cada consulta. Recomende {'particao': coluna mais filtrada, 'cluster': 2a mais filtrada} (empate: ordem alfabetica). Se so houver uma coluna, cluster = None.

```bash
cd modulos/06-data-warehousing-bigquery/exercicio-10
pytest -q
```

## Dica
:::{dropdown} Dica
conte a frequencia de cada coluna nos filtros; a mais frequente vira particao, a 2a vira cluster.
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def layout_recomendado(consultas):
    from collections import Counter
    c = Counter()
    for cols in consultas:
        for col in cols:
            c[col] += 1
    ranked = sorted(c, key=lambda k: (-c[k], k))
    return {'particao': ranked[0] if ranked else None, 'cluster': ranked[1] if len(ranked) > 1 else None}
```
:::

---
**Revisado em:** 2026-09-09
