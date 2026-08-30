# Exercício 06 — Retry para rate limit / falhas (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

APIs falham de forma **transitória** (429 rate limit, timeout). Implemente o **retry** que
torna a ingestão resiliente.

## Tarefa
Em [`exercicio-06/solucao.py`](exercicio-06/solucao.py):

- **`com_retry(fn, tentativas=3)`** — chame `fn()`; se levantar exceção, tente de novo até
  `tentativas` chamadas no total. Retorne no primeiro sucesso; se esgotar, **relance** a última exceção.

```bash
cd modulos/08-ingestao-integracao/exercicio-06
pytest -q
```

> Na prática, entre as tentativas você espera cada vez mais (**backoff exponencial** + jitter),
> respeitando o rate limit. Aqui focamos na mecânica do retry.

## Dicas progressivas
:::{dropdown} Dica 1 — o laço
`for i in range(tentativas): try: return fn() except Exception: guarde e continue`.
:::
:::{dropdown} Dica 2 — relançar
Depois do laço, `raise` a última exceção capturada.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def com_retry(fn, tentativas=3):
    ultima = None
    for _ in range(tentativas):
        try:
            return fn()
        except Exception as e:  # noqa: BLE001
            ultima = e
    raise ultima
```
Cada tentativa reexecuta `fn`; no sucesso, retorna. Esgotando, relança o último erro. Num
extrator real, você adicionaria `time.sleep(2 ** tentativa)` (backoff) e trataria só erros
transitórios (429/5xx), deixando 4xx "de verdade" falharem na hora.
:::

---
**Revisado em:** 2026-08-29
