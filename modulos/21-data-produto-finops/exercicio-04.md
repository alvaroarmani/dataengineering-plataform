# Exercício 04 — TCO (custo total de propriedade) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py): implemente **`tco`** — O TCO soma o custo inicial com os custos recorrentes no período. Retorne custo_inicial + custo_mensal * meses.

```bash
cd modulos/21-data-produto-finops/exercicio-04
pytest -q
```

## Dica
:::{dropdown} Dica
TCO = inicial + mensal * meses.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def tco(custo_inicial, custo_mensal, meses):
    return custo_inicial + custo_mensal * meses
```
:::

---
**Revisado em:** 2026-08-31
