# Exercicio 06 - Componente conexa (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-06/solucao.py`](exercicio-06/solucao.py): implemente **`componente`** - Retorne a lista ORDENADA de todos os nos alcancaveis a partir de `no` (incluindo ele mesmo) — a componente conexa.

```bash
cd modulos/22-grafos-conhecimento/exercicio-06
pytest -q
```

## Dica
:::{dropdown} Dica
DFS/BFS acumulando os alcancaveis a partir de `no` (inclui ele mesmo).
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def componente(grafo, no):
    vistos = set()
    pilha = [no]
    while pilha:
        atual = pilha.pop()
        if atual not in vistos:
            vistos.add(atual)
            pilha.extend(grafo.get(atual, []))
    return sorted(vistos)
```
:::

---
**Revisado em:** 2026-09-09
