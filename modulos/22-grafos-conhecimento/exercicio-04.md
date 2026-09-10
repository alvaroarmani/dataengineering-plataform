# Exercicio 04 - Amigos em comum (recomendacao) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py): implemente **`amigos_em_comum`** - Retorne a lista ORDENADA dos vizinhos que `a` e `b` tem em comum (base de 'pessoas que voce talvez conheca').

```bash
cd modulos/22-grafos-conhecimento/exercicio-04
pytest -q
```

## Dica
:::{dropdown} Dica
intersecao dos conjuntos de vizinhos de a e b, ordenada.
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def amigos_em_comum(grafo, a, b):
    return sorted(set(grafo.get(a, [])) & set(grafo.get(b, [])))
```
:::

---
**Revisado em:** 2026-09-09
