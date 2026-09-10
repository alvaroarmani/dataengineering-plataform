# Exercicio 09 - Merge incremental com dado atrasado (nivel avancado)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro). Aplica a [teoria 05](teoria-05-dbt-avancado-incremental.md).

## Tarefa
Em [`exercicio-09/solucao.py`](exercicio-09/solucao.py): implemente **`merge_incremental`** - Estrategia incremental 'merge' com protecao contra dado atrasado. destino e batch = listas de dicts com a `chave`, 'valor' e 'updated_at'. Faca upsert do batch no destino: insira chaves novas e ATUALIZE existentes SOMENTE se o updated_at do batch for >= o do destino (registro atrasado/antigo NAO sobrescreve). Retorne a lista final ordenada por `chave`.

```bash
cd modulos/07-transformacao-dbt/exercicio-09
pytest -q
```

## Dica
:::{dropdown} Dica
indexe o destino por chave; para cada linha do batch, upsert so se updated_at >= o existente.
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def merge_incremental(destino, batch, chave):
    por_chave = {r[chave]: r for r in destino}
    for r in batch:
        k = r[chave]
        if k not in por_chave or r['updated_at'] >= por_chave[k]['updated_at']:
            por_chave[k] = r
    return sorted(por_chave.values(), key=lambda r: r[chave])
```
:::

---
**Revisado em:** 2026-09-09
