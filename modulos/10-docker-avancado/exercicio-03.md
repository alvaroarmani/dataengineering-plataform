# Exercício 03 — Ordem de subida (depends_on) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-03/solucao.py`](exercicio-03/solucao.py): implemente **`ordem_subida`** — o serviço que ninguém depende sobe primeiro (grau de entrada 0); é o algoritmo de Kahn.

```bash
cd modulos/10-docker-avancado/exercicio-03
pytest -q
```

## Dica
:::{dropdown} Dica
Kahn: comece pelos de grau 0, libere os dependentes.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def ordem_subida(servicos, depends_on):
    from collections import defaultdict
    dep = defaultdict(int); saintes = defaultdict(list)
    for a, b in depends_on:
        dep[b] += 1; saintes[a].append(b)
    fila = [s for s in servicos if dep[s] == 0]; ordem = []
    while fila:
        s = fila.pop(0); ordem.append(s)
        for viz in saintes[s]:
            dep[viz] -= 1
            if dep[viz] == 0:
                fila.append(viz)
    return ordem
```
:::

---
**Revisado em:** 2026-08-29
