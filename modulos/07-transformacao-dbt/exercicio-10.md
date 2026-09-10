# Exercicio 10 - Selecao incremental por watermark (nivel avancado)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro). Aplica a [teoria 05](teoria-05-dbt-avancado-incremental.md).

## Tarefa
Em [`exercicio-10/solucao.py`](exercicio-10/solucao.py): implemente **`selecionar_incremental`** - O filtro `is_incremental()` do dbt. linhas = lista de dicts com 'updated_at'. Retorne uma TUPLA (novas, novo_watermark): novas = as linhas com updated_at > watermark (na ordem de entrada); novo_watermark = o maior updated_at entre TODAS as linhas (ou o proprio watermark se nao houver linhas).

```bash
cd modulos/07-transformacao-dbt/exercicio-10
pytest -q
```

## Dica
:::{dropdown} Dica
filtre updated_at > watermark preservando a ordem; o novo watermark e o max de todos.
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def selecionar_incremental(linhas, watermark):
    novas = [r for r in linhas if r['updated_at'] > watermark]
    novo = max((r['updated_at'] for r in linhas), default=watermark)
    return (novas, novo)
```
:::

---
**Revisado em:** 2026-09-09
