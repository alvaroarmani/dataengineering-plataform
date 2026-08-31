# Exercício 06 — Exactly-once por dedup (idempotência) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-06/solucao.py`](exercicio-06/solucao.py): implemente **`processar_idempotente`** — eventos = lista de (id, valor), podendo repetir id (reentrega). Processe cada id UMA vez (a 1ª ocorrência vence) e retorne a soma dos valores — reprocessar não infla o total.

```bash
cd modulos/17-streaming-tempo-real/exercicio-06
pytest -q
```

## Dica
:::{dropdown} Dica
guarde os ids já vistos num set; só some o valor da 1ª vez que cada id aparece.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def processar_idempotente(eventos):
    vistos = set()
    total = 0
    for eid, valor in eventos:
        if eid not in vistos:
            vistos.add(eid)
            total += valor
    return total
```
:::

---
**Revisado em:** 2026-08-31
