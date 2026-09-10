# Exercicio 05 - No mais conectado (centralidade) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-05/solucao.py`](exercicio-05/solucao.py): implemente **`mais_conectado`** - Retorne o no de MAIOR grau; em empate, o de menor nome (ordem alfabetica).

```bash
cd modulos/22-grafos-conhecimento/exercicio-05
pytest -q
```

## Dica
:::{dropdown} Dica
ordene por (-grau, nome) e pegue o primeiro.
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def mais_conectado(grafo):
    return sorted(grafo, key=lambda n: (-len(grafo[n]), n))[0]
```
:::

---
**Revisado em:** 2026-09-09
