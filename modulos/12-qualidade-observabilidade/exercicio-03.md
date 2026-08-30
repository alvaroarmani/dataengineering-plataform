# Exercício 03 — Unicidade: chaves duplicadas (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-03/solucao.py`](exercicio-03/solucao.py): implemente **`duplicados`** — Retorne a lista ORDENADA de valores que aparecem MAIS DE UMA VEZ.

```bash
cd modulos/12-qualidade-observabilidade/exercicio-03
pytest -q
```

## Dica
:::{dropdown} Dica
use Counter e filtre contagem > 1.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def duplicados(chaves):
    from collections import Counter
    return sorted(v for v, n in Counter(chaves).items() if n > 1)
```
:::

---
**Revisado em:** 2026-08-29
