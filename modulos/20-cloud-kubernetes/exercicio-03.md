# Exercício 03 — Deployment saudável? (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-03/solucao.py`](exercicio-03/solucao.py): implemente **`deployment_saudavel`** — Um Deployment do Kubernetes está saudável quando o número de pods PRONTOS atinge (ou passa) o DESEJADO. Retorne o booleano.

```bash
cd modulos/20-cloud-kubernetes/exercicio-03
pytest -q
```

## Dica
:::{dropdown} Dica
prontos >= desejado.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def deployment_saudavel(desejado, prontos):
    return prontos >= desejado
```
:::

---
**Revisado em:** 2026-08-31
