# Exercício 01 — Pode fazer merge? (CI verde) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-01/solucao.py`](exercicio-01/solucao.py): implemente **`pode_mergear`** — checks = lista de (nome, status). True se TODOS os status forem 'pass'.

```bash
cd modulos/13-dataops-cicd-iac/exercicio-01
pytest -q
```

## Dica
:::{dropdown} Dica
all(status == 'pass' ...).
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def pode_mergear(checks):
    return all(s == 'pass' for _, s in checks)
```
:::

---
**Revisado em:** 2026-08-29
