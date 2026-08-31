# Exercício 03 — Expiração de cache (TTL) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-03/solucao.py`](exercicio-03/solucao.py): implemente **`expirou`** — Em key-value com TTL, uma chave expira quando o tempo desde a gravação atinge o TTL. Retorne True se (agora - gravado_em) >= ttl_seg.

```bash
cd modulos/18-nosql-nao-relacional/exercicio-03
pytest -q
```

## Dica
:::{dropdown} Dica
compare a idade (agora - gravado_em) com o ttl_seg.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def expirou(agora, gravado_em, ttl_seg):
    return (agora - gravado_em) >= ttl_seg
```
:::

---
**Revisado em:** 2026-08-31
