# Exercício 04 — Receita por categoria com pandas (com pytest)

**Onde roda:** 🟢 Browser ou 🐳 Bancada Docker (usa pandas).

Limpar + agregar é o combo mais comum em pandas. Aqui você trata `NaN` e usa `groupby`.

## Tarefa

Implemente, em [`exercicio-04/solucao.py`](exercicio-04/solucao.py), a função
`receita_por_categoria(df)` que recebe um `DataFrame` com as colunas `categoria` e `valor`
(que pode conter `NaN`) e retorna um **novo DataFrame** com:

- colunas **`categoria`** e **`receita`** (soma dos valores por categoria);
- **ignorando** linhas com `valor` nulo;
- ordenado por **`receita` decrescente**;
- com índice **reiniciado** (0, 1, 2…).

```bash
cd modulos/03-python-eng-dados/exercicio-04
pytest -q
```

Exemplo:
```python
import pandas as pd, numpy as np
df = pd.DataFrame({"categoria": ["a", "b", "a"], "valor": [10.0, np.nan, 5.0]})
receita_por_categoria(df)
#   categoria  receita
# 0         a     15.0
# 1         b      0.0   (b só tinha NaN -> não aparece)  ← ver dica
```

## Dicas progressivas
:::{dropdown} Dica 1 — limpar
`df.dropna(subset=["valor"])` remove as linhas com valor nulo.
:::
:::{dropdown} Dica 2 — agregar e formatar
`groupby("categoria")["valor"].sum()` dá uma Series; use `.reset_index()` e renomeie a coluna para `receita`.
:::
:::{dropdown} Dica 3 — ordenar
`.sort_values("receita", ascending=False).reset_index(drop=True)`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def receita_por_categoria(df):
    limpo = df.dropna(subset=["valor"])
    out = (
        limpo.groupby("categoria")["valor"].sum()
        .reset_index()
        .rename(columns={"valor": "receita"})
        .sort_values("receita", ascending=False)
        .reset_index(drop=True)
    )
    return out
```
`dropna` remove os nulos **antes** de agregar (categorias que só tinham `NaN` somem, pois
não há linha para agrupar). O `groupby().sum()` faz o split-apply-combine; `reset_index`
transforma a Series de volta em DataFrame; ordenamos e reiniciamos o índice para uma saída limpa.
:::

---
**Revisado em:** 2026-08-22
