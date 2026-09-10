# Exercicio 02 - Grau de um no (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-02/solucao.py`](exercicio-02/solucao.py): implemente **`grau`** - Retorne o GRAU de `no` = quantidade de vizinhos (arestas incidentes).

```bash
cd modulos/22-grafos-conhecimento/exercicio-02
pytest -q
```

## Dica
:::{dropdown} Dica
grau = numero de vizinhos = len(grafo.get(no, [])).
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def grau(grafo, no):
    return len(grafo.get(no, []))
```
:::

---
**Revisado em:** 2026-09-09
