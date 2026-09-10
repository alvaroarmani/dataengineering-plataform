# Exercicio 14 - Particoes varridas (partition pruning) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-14/solucao.py`](exercicio-14/solucao.py): implemente **`particoes_varridas`** - particoes = lista de (min, max) de cada particao. Com um filtro no intervalo [lo, hi], retorne QUANTAS particoes precisam ser lidas (as que se sobrepoem ao intervalo) — o resto e podado.

```bash
cd modulos/04-sql-bancos-relacionais/exercicio-14
pytest -q
```

## Dica
:::{dropdown} Dica
uma particao (pmin,pmax) se sobrepoe a [lo,hi] se NAO (pmax<lo ou pmin>hi).
:::

## Solucao comentada (abra so DEPOIS de passar)
:::{dropdown} Ver solucao comentada
```python
def particoes_varridas(particoes, lo, hi):
    return sum(1 for pmin, pmax in particoes if not (pmax < lo or pmin > hi))
```
:::

---
**Revisado em:** 2026-09-09
