# Exercicio 03 - Distancia em saltos (BFS) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-03/solucao.py`](exercicio-03/solucao.py): implemente **`distancia_em_saltos`** - Retorne o menor numero de saltos de `origem` a `destino` (BFS). 0 se forem iguais; -1 se nao houver caminho.

```bash
cd modulos/22-grafos-conhecimento/exercicio-03
pytest -q
```

## Dica
:::{dropdown} Dica
BFS por niveis: a distancia e o nivel em que o destino aparece; sem alcance, -1.
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def distancia_em_saltos(grafo, origem, destino):
    if origem == destino:
        return 0
    from collections import deque
    vistos = {origem}
    fila = deque([(origem, 0)])
    while fila:
        atual, d = fila.popleft()
        for viz in grafo.get(atual, []):
            if viz == destino:
                return d + 1
            if viz not in vistos:
                vistos.add(viz)
                fila.append((viz, d + 1))
    return -1
```
:::

---
**Revisado em:** 2026-09-09
