# Exercício 04 — Autoscaling (HPA) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py): implemente **`hpa_replicas`** — O HorizontalPodAutoscaler ajusta réplicas pela fórmula: desejado = ceil(replicas_atuais * cpu_atual / cpu_alvo). Retorne o número desejado de réplicas.

```bash
cd modulos/20-cloud-kubernetes/exercicio-04
pytest -q
```

## Dica
:::{dropdown} Dica
aplique ceil(replicas * cpu_atual / cpu_alvo) com -(-a // b).
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def hpa_replicas(replicas_atuais, cpu_atual, cpu_alvo):
    return -(-(replicas_atuais * cpu_atual) // cpu_alvo)
```
:::

---
**Revisado em:** 2026-08-31
