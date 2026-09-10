# Exercicio 09 - Ordem topologica do DAG (nivel avancado)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro). Aplica a [teoria 05](teoria-05-airflow-avancado.md).

## Tarefa
Em [`exercicio-09/solucao.py`](exercicio-09/solucao.py): implemente **`ordem_topologica`** - O scheduler roda as tasks em ordem topologica. grafo = {task: [dependencias (upstream)]}. Retorne uma ordem valida de execucao (toda task apos suas dependencias); em empate, ordem alfabetica. Se houver ciclo, retorne None.

```bash
cd modulos/09-orquestracao-airflow/exercicio-09
pytest -q
```

## Dica
:::{dropdown} Dica
Kahn: comece pelas tasks sem dependencia (indeg 0), use um heap p/ desempate alfabetico; se sobrar task, ha ciclo -> None.
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def ordem_topologica(grafo):
    import heapq
    indeg = {t: len(deps) for t, deps in grafo.items()}
    dependentes = {t: [] for t in grafo}
    for t, deps in grafo.items():
        for d in deps:
            dependentes[d].append(t)
    heap = [t for t in grafo if indeg[t] == 0]
    heapq.heapify(heap)
    ordem = []
    while heap:
        n = heapq.heappop(heap)
        ordem.append(n)
        for m in dependentes[n]:
            indeg[m] -= 1
            if indeg[m] == 0:
                heapq.heappush(heap, m)
    return ordem if len(ordem) == len(grafo) else None
```
:::

---
**Revisado em:** 2026-09-09
