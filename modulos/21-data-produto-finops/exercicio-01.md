# Exercício 01 — Custo de uma consulta (bytes varridos) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-01/solucao.py`](exercicio-01/solucao.py): implemente **`custo_consulta`** — No modelo pay-per-scan (BigQuery), a consulta custa pelos TB varridos. Retorne o custo = tb_varridos * preco_por_tb.

```bash
cd modulos/21-data-produto-finops/exercicio-01
pytest -q
```

## Dica
:::{dropdown} Dica
custo = TB varridos * preço por TB.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def custo_consulta(tb_varridos, preco_por_tb):
    return tb_varridos * preco_por_tb
```
:::

---
**Revisado em:** 2026-08-31
