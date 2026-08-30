# Exercício 07 — Retries do Airflow (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

No Airflow, `retries=N` faz a task tentar até **N+1** vezes. Implemente essa política.

## Tarefa
Em [`exercicio-07/solucao.py`](exercicio-07/solucao.py):

- **`executar_com_retries(fn, retries)`** — retorne `(True, k)` se `fn` passou na k-ésima
  tentativa, ou `(False, N+1)` se falhou em todas (`retries=N` ⇒ até `N+1` tentativas).

```bash
cd modulos/09-orquestracao-airflow/exercicio-07
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — o laço
`for tentativa in range(1, retries+2): try: fn(); return (True, tentativa) except: continue`.
:::
:::{dropdown} Dica 2 — esgotou
Fora do laço, `return (False, retries+1)`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def executar_com_retries(fn, retries):
    for tentativa in range(1, retries + 2):   # 1 original + N retries
        try:
            fn()
            return (True, tentativa)
        except Exception:  # noqa: BLE001
            continue
    return (False, retries + 1)
```
É a semântica de `retries`/`retry_delay` do Airflow: falhas transitórias são reexecutadas
automaticamente. Só é seguro porque a task é **idempotente** (U3) — senão o retry duplicaria dados.
:::

---
**Revisado em:** 2026-08-29
