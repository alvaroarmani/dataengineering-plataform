# Exercício 05 — Freshness: dentro do SLA? (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-05/solucao.py`](exercicio-05/solucao.py): implemente **`esta_fresco`** — Datas 'AAAA-MM-DD HH:MM'. True se (agora - ultima) <= sla_horas.

```bash
cd modulos/12-qualidade-observabilidade/exercicio-05
pytest -q
```

## Dica
:::{dropdown} Dica
diferença em horas entre agora e ultima; compare com o SLA.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def esta_fresco(ultima, agora, sla_horas):
    from datetime import datetime
    f='%Y-%m-%d %H:%M'
    dif=(datetime.strptime(agora,f)-datetime.strptime(ultima,f)).total_seconds()/3600
    return dif <= sla_horas
```
:::

---
**Revisado em:** 2026-08-29
