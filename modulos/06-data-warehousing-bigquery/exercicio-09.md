# Exercicio 09 - Bytes varridos (poda coluna x particao) (nivel avancado)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro). Aplica a [teoria 05](teoria-05-otimizacao-consultas-avancada.md).

## Tarefa
Em [`exercicio-09/solucao.py`](exercicio-09/solucao.py): implemente **`bytes_varridos`** - Estime os bytes varridos por uma consulta num DW colunar particionado: (soma dos bytes das colunas lidas) * (particoes_lidas / particoes_total). bytes_por_coluna = {coluna: bytes}. Retorne float.

```bash
cd modulos/06-data-warehousing-bigquery/exercicio-09
pytest -q
```

## Dica
:::{dropdown} Dica
some os bytes das colunas do SELECT e multiplique pela fracao de particoes lidas.
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def bytes_varridos(bytes_por_coluna, colunas_lidas, particoes_total, particoes_lidas):
    total_colunas = sum(bytes_por_coluna[c] for c in colunas_lidas)
    return total_colunas * (particoes_lidas / particoes_total)
```
:::

---
**Revisado em:** 2026-09-09
