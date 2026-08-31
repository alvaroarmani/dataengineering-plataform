# Exercício 05 — Cumpre o SLA? (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-05/solucao.py`](exercicio-05/solucao.py): implemente **`cumpre_sla`** — Um data product tem um SLA de disponibilidade (ex.: 99.9%). Retorne True se o uptime real atingir (ou passar) o alvo.

```bash
cd modulos/21-data-produto-finops/exercicio-05
pytest -q
```

## Dica
:::{dropdown} Dica
cumpre se uptime_real >= sla_alvo.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def cumpre_sla(uptime_real, sla_alvo):
    return uptime_real >= sla_alvo
```
:::

---
**Revisado em:** 2026-08-31
