# Exercício 03 — ROI de um projeto de dados (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-03/solucao.py`](exercicio-03/solucao.py): implemente **`roi`** — Retorne o ROI = (retorno - investimento) / investimento (ex.: 2.0 = 200% de retorno sobre o investido).

```bash
cd modulos/21-data-produto-finops/exercicio-03
pytest -q
```

## Dica
:::{dropdown} Dica
ROI = (retorno - investimento) / investimento.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def roi(retorno, investimento):
    return (retorno - investimento) / investimento
```
:::

---
**Revisado em:** 2026-08-31
