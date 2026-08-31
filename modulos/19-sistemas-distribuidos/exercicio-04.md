# Exercício 04 — Consenso por maioria (quórum) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py): implemente **`tem_consenso`** — Uma decisão só passa com a MAIORIA estrita dos nós. Retorne True se `a_favor` > metade de `total`.

```bash
cd modulos/19-sistemas-distribuidos/exercicio-04
pytest -q
```

## Dica
:::{dropdown} Dica
maioria estrita: a_favor > total/2 (empate não é maioria).
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def tem_consenso(a_favor, total):
    return a_favor > total / 2
```
:::

---
**Revisado em:** 2026-08-31
