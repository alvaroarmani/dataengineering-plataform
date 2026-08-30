# Exercício 01 — Ordem topológica de uma DAG (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

O Airflow roda as tasks em **ordem topológica** (dependências primeiro). Implemente essa ordem.

## Tarefa
Em [`exercicio-01/solucao.py`](exercicio-01/solucao.py):

- **`ordem_topologica(tasks, arestas)`** — `arestas` = lista de `(a, b)` ("b depende de a").
  Retorne todas as tasks numa ordem que respeite as dependências.

```bash
cd modulos/09-orquestracao-airflow/exercicio-01
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — algoritmo de Kahn
Conte o **grau de entrada** (dependências) de cada task; comece pelas de grau 0; ao "remover" uma, decremente os vizinhos e adicione os que zeraram.
:::
:::{dropdown} Dica 2 — ordem estável
Processe as tasks na ordem em que aparecem em `tasks` para uma saída previsível.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def ordem_topologica(tasks, arestas):
    from collections import defaultdict
    dep = defaultdict(int)                 # grau de entrada
    saintes = defaultdict(list)
    for a, b in arestas:
        dep[b] += 1
        saintes[a].append(b)
    fila = [t for t in tasks if dep[t] == 0]
    ordem = []
    while fila:
        t = fila.pop(0)
        ordem.append(t)
        for viz in saintes[t]:
            dep[viz] -= 1
            if dep[viz] == 0:
                fila.append(viz)
    return ordem
```
É o **algoritmo de Kahn**: começa pelas tasks sem dependências e vai liberando as demais. É
exatamente o raciocínio do scheduler do Airflow para decidir o que pode rodar.
:::

---
**Revisado em:** 2026-08-29
