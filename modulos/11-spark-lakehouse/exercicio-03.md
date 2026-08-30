# Exercício 03 — Agregação de um DataFrame (receita por categoria) (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

## Tarefa
Em [`exercicio-03/solucao.py`](exercicio-03/solucao.py): implemente **`receita_por_categoria`** — some preco*qtd por categoria e ordene por receita desc, categoria.

```bash
cd modulos/11-spark-lakehouse/exercicio-03
pytest -q
```

## Dica
:::{dropdown} Dica
Acumule num dict e ordene.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def receita_por_categoria(linhas):
    from collections import defaultdict
    tot = defaultdict(int)
    for r in linhas:
        tot[r['categoria']] += r['preco'] * r['qtd']
    return sorted(tot.items(), key=lambda kv: (-kv[1], kv[0]))
```
:::

---
**Revisado em:** 2026-08-29
