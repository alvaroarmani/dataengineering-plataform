# Exercício 04 — O modelo de custo do DW cloud (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

Implemente o modelo de custo *por bytes varridos* — a base para raciocinar sobre o preço de
uma query no BigQuery on-demand.

## Tarefas
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py):

- **`bytes_varridos(colunas_lidas, particoes_lidas, bytes_por_coluna)`** — soma dos bytes das
  colunas lidas (do dict `bytes_por_coluna`), vezes o nº de partições lidas.
- **`custo_usd(bytes, preco_por_tb=6.25)`** — custo em US$ (1 TB = 1e12 bytes).

```bash
cd modulos/06-data-warehousing-bigquery/exercicio-04
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1
`sum(bytes_por_coluna[c] for c in colunas_lidas) * particoes_lidas`.
:::
:::{dropdown} Dica 2
`bytes / 1e12 * preco_por_tb`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def bytes_varridos(colunas_lidas, particoes_lidas, bytes_por_coluna):
    return sum(bytes_por_coluna[c] for c in colunas_lidas) * particoes_lidas

def custo_usd(bytes_varridos_total, preco_por_tb=6.25):
    return bytes_varridos_total / 1e12 * preco_por_tb
```
Este é exatamente o raciocínio do dry run: menos colunas e menos partições ⇒ menos bytes ⇒
menos custo. É por isso que `SELECT *` sem filtro é caro.
:::

---
**Revisado em:** 2026-08-24
