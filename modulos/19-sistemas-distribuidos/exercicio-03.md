# Exercício 03 — Tolerância a falhas (2f+1) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-03/solucao.py`](exercicio-03/solucao.py): implemente **`tolera_falhas`** — Um sistema de consenso com N réplicas tolera a falha de f nós enquanto a maioria sobrevive: N = 2f+1. Retorne quantas falhas (f) ele tolera.

```bash
cd modulos/19-sistemas-distribuidos/exercicio-03
pytest -q
```

## Dica
:::{dropdown} Dica
f = (N - 1) // 2 — a maioria precisa sobreviver.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def tolera_falhas(replicas):
    return (replicas - 1) // 2
```
:::

---
**Revisado em:** 2026-08-31
