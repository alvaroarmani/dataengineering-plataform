# Exercício 04 — Lag total do consumidor (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py): implemente **`lag_total`** — fim e commit são {particao: offset}. O lag de uma partição é fim - offset commitado. Retorne o lag TOTAL (soma) do consumidor. Partição sem commit conta a partir de 0.

```bash
cd modulos/17-streaming-tempo-real/exercicio-04
pytest -q
```

## Dica
:::{dropdown} Dica
para cada partição em fim, some fim - commit.get(p,0).
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def lag_total(fim, commit):
    return sum(fim[p] - commit.get(p, 0) for p in fim)
```
:::

---
**Revisado em:** 2026-08-31
