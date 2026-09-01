# Exercicio 04 - Qual arquitetura de dados? (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-04/solucao.py`](exercicio-04/solucao.py): implemente **`arquitetura_recomendada`** - Recomende: sql_estruturado -> 'data-warehouse'; dados_brutos/variados -> 'data-lake'; ambos -> 'lakehouse'; senao 'data-warehouse'.

```bash
cd modulos/01-fundamentos-eng-dados/exercicio-04
pytest -q
```

## Dica
:::{dropdown} Dica
dict de caso->arquitetura, com default data-warehouse.
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def arquitetura_recomendada(caso):
    mapa = {'sql_estruturado': 'data-warehouse', 'dados_brutos': 'data-lake', 'variados': 'data-lake', 'ambos': 'lakehouse'}
    return mapa.get(caso, 'data-warehouse')
```
:::

---
**Revisado em:** 2026-08-31
