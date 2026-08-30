# Exercício 08 — Estado de um DAG run (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

Observabilidade começa por saber **se o run passou**. Resuma o estado a partir das tasks.

## Tarefa
Em [`exercicio-08/solucao.py`](exercicio-08/solucao.py):

- **`estado_do_run(tasks)`** — `tasks` = lista de `(nome, status)`. Retorne
  `{'success': n, 'failed': n, 'skipped': n, 'run_ok': bool}`, com `run_ok` True só se **nenhuma** falhou.

```bash
cd modulos/09-orquestracao-airflow/exercicio-08
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — conte
`Counter(status for _, status in tasks)` e leia cada chave (com default 0).
:::
:::{dropdown} Dica 2 — run_ok
`run_ok = (falhas == 0)`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
from collections import Counter

def estado_do_run(tasks):
    c = Counter(status for _, status in tasks)
    falhas = c.get("failed", 0)
    return {
        "success": c.get("success", 0),
        "failed": falhas,
        "skipped": c.get("skipped", 0),
        "run_ok": falhas == 0,
    }
```
É o que o Airflow mostra na UI: o **DAG run** é `failed` se qualquer task falhou (após os
retries), senão `success`. Monitorar isso (e alertar no failure) é a base da observabilidade.
:::

---
**Revisado em:** 2026-08-29
