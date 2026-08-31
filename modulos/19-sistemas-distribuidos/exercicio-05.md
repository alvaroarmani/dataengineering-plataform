# Exercício 05 — Réplica atrasada (replication lag) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-05/solucao.py`](exercicio-05/solucao.py): implemente **`replica_atrasada`** — O lag de replicação é offset_lider - offset_replica. Retorne True se o lag ultrapassar `limite` (réplica velha demais para leitura consistente).

```bash
cd modulos/19-sistemas-distribuidos/exercicio-05
pytest -q
```

## Dica
:::{dropdown} Dica
lag = lider - replica; atrasada se lag > limite.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def replica_atrasada(offset_lider, offset_replica, limite):
    return (offset_lider - offset_replica) > limite
```
:::

---
**Revisado em:** 2026-08-31
