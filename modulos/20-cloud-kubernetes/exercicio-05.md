# Exercício 05 — Cabe no nó? (scheduler) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-05/solucao.py`](exercicio-05/solucao.py): implemente **`cabe_no_no`** — pods_cpu = lista de CPU requisitada por cada pod. Retorne True se a soma das requisições couber na capacidade `cpu_no` do nó.

```bash
cd modulos/20-cloud-kubernetes/exercicio-05
pytest -q
```

## Dica
:::{dropdown} Dica
some as requisições e compare com a capacidade do nó.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def cabe_no_no(pods_cpu, cpu_no):
    return sum(pods_cpu) <= cpu_no
```
:::

---
**Revisado em:** 2026-08-31
