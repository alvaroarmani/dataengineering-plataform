# Exercício 01 — Impact analysis (lineage a jusante) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-01/solucao.py`](exercicio-01/solucao.py): implemente **`impactados`** — grafo = {tabela: [dependentes...]}. Retorne a lista ORDENADA de todas as tabelas a jusante (transitivas) de `tabela`, sem incluir ela mesma.

```bash
cd modulos/14-governanca-seguranca-lgpd/exercicio-01
pytest -q
```

## Dica
:::{dropdown} Dica
BFS/DFS a partir dos dependentes de `tabela`; acumule tudo que alcançar e ordene.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def impactados(grafo, tabela):
    vistos = set()
    fila = list(grafo.get(tabela, []))
    while fila:
        t = fila.pop()
        if t not in vistos:
            vistos.add(t)
            fila.extend(grafo.get(t, []))
    return sorted(vistos)
```
:::

---
**Revisado em:** 2026-08-29
