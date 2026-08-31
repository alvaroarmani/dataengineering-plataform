# Exercício 06 — DNS de service (service discovery) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-06/solucao.py`](exercicio-06/solucao.py): implemente **`dns_servico`** — No Kubernetes, um Service é resolvido pelo DNS interno como '<servico>.<namespace>.svc.cluster.local'. Monte e retorne esse nome.

```bash
cd modulos/20-cloud-kubernetes/exercicio-06
pytest -q
```

## Dica
:::{dropdown} Dica
formate '<servico>.<namespace>.svc.cluster.local'.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def dns_servico(servico, namespace):
    return f'{servico}.{namespace}.svc.cluster.local'
```
:::

---
**Revisado em:** 2026-08-31
