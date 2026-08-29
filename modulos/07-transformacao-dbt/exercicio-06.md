# Exercício 06 — Os testes do dbt "por baixo" (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (Python puro).

Um teste dbt é só **uma query que busca violações** (0 = passa). Implemente, em Python, a
lógica que sustenta `relationships` e `unique` — assim você entende o que o dbt faz por baixo.

## Tarefas
Em [`exercicio-06/solucao.py`](exercicio-06/solucao.py):

- **`orfaos(fato_produto_ids, dim_produto_ids)`** — (`relationships`) lista ordenada, sem
  repetição, dos `produto_id` que aparecem no fato mas **não** existem na dimensão.
- **`duplicados(valores)`** — (`unique`) lista ordenada dos valores que aparecem **mais de uma vez**.

```bash
cd modulos/07-transformacao-dbt/exercicio-06
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — órfãos
`sorted({p for p in fato_produto_ids if p not in set(dim_produto_ids)})`.
:::
:::{dropdown} Dica 2 — duplicados
Use `collections.Counter` e filtre os que têm contagem > 1.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
from collections import Counter

def orfaos(fato_produto_ids, dim_produto_ids):
    validos = set(dim_produto_ids)
    return sorted({p for p in fato_produto_ids if p not in validos})

def duplicados(valores):
    return sorted(v for v, n in Counter(valores).items() if n > 1)
```
`orfaos` é exatamente o que o teste `relationships` roda (violações de FK); `duplicados` é o
que `unique` procura. Em ambos, **0 resultados = teste passa**.
:::

---
**Revisado em:** 2026-08-24
