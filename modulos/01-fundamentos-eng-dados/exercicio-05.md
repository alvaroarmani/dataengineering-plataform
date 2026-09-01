# Exercicio 05 - Vantagem do colunar (bytes lidos) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-05/solucao.py`](exercicio-05/solucao.py): implemente **`bytes_colunar`** - No armazenamento colunar, a consulta le SO as colunas necessarias. Retorne os bytes lidos = lidas * bytes_por_coluna (independente do total de colunas).

```bash
cd modulos/01-fundamentos-eng-dados/exercicio-05
pytest -q
```

## Dica
:::{dropdown} Dica
colunar le so as colunas pedidas: lidas * bytes_por_coluna.
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def bytes_colunar(total_colunas, lidas, bytes_por_coluna):
    return lidas * bytes_por_coluna
```
:::

---
**Revisado em:** 2026-08-31
