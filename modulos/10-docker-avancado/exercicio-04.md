# Exercício 04 — Mapeamento de portas (host:container) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py): implemente **`porta_host`** — `ports: host:container` — ache o mapeamento cujo lado container bate.

```bash
cd modulos/10-docker-avancado/exercicio-04
pytest -q
```

## Dica
:::{dropdown} Dica
Faça split(':') e compare o lado do container.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def porta_host(mapa, porta_container):
    for m in mapa:
        h, c = m.split(':')
        if int(c) == porta_container:
            return int(h)
    return None
```
:::

---
**Revisado em:** 2026-08-29
