# Exercicio 01 - Vizinhos de um no (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-01/solucao.py`](exercicio-01/solucao.py): implemente **`vizinhos`** - grafo = {no: [vizinhos]} (lista de adjacencia). Retorne a lista ORDENADA dos vizinhos de `no` (vazia se nao existir).

```bash
cd modulos/22-grafos-conhecimento/exercicio-01
pytest -q
```

## Dica
:::{dropdown} Dica
sorted(grafo.get(no, [])).
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def vizinhos(grafo, no):
    return sorted(grafo.get(no, []))
```
:::

---
**Revisado em:** 2026-09-09
