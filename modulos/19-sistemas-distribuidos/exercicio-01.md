# Exercício 01 — Custo de armazenamento com replicação (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-01/solucao.py`](exercicio-01/solucao.py): implemente **`custo_replicacao`** — Com fator de replicação, cada dado é guardado em `fator` réplicas. Retorne o armazenamento total (GB) para `dados_gb` de dados.

```bash
cd modulos/19-sistemas-distribuidos/exercicio-01
pytest -q
```

## Dica
:::{dropdown} Dica
armazenamento total = dados * fator de replicação.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def custo_replicacao(dados_gb, fator):
    return dados_gb * fator
```
:::

---
**Revisado em:** 2026-08-31
