# Exercício 03 — groupBy com a semântica de nulos do Spark

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
`df.groupBy("categoria").agg(F.sum("valor"), F.count("valor"), F.count("*"), F.avg("valor"))` parece
óbvio, até aparecer `null`. A semântica do Spark (a mesma do SQL) tem regras que pegam muita gente:
`count("*")` conta **linhas**, `count("valor")` conta só os **não nulos**, `sum` e `avg` **ignoram** nulos
(a média é sobre os não nulos, não sobre todas as linhas), e a soma de um grupo **só com nulos** é `null`,
não zero. E `null` na chave de agrupamento forma um **grupo próprio**.

## Tarefa
Em [`exercicio-03/solucao.py`](exercicio-03/solucao.py), implemente `agregar(linhas, chave, coluna)`.

```bash
cd modulos/11-spark-lakehouse/exercicio-03
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — agrupe com get
`grupos.setdefault(l.get(chave), []).append(l.get(coluna))` — chave ausente e chave `None` caem no mesmo grupo, como no Spark.
:::
:::{dropdown} Dica 2 — não nulos
Para cada grupo: `linhas` é o total; `n`, `soma`, `media` e `maximo` usam só `[v for v in valores if v is not None]` — e viram `None` se essa lista estiver vazia.
:::
:::{dropdown} Dica 3 — ordenar com None por último
Uma chave de ordenação `(x is None, x)` põe os `None` no fim (use um valor substituto no lugar do `None` para não comparar `None` com texto).
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def agregar(linhas: list, chave: str, coluna: str) -> list:
    grupos = {}
    for l in linhas:
        grupos.setdefault(l.get(chave), []).append(l.get(coluna))
    saida = []
    for k in sorted(grupos, key=lambda x: (x is None, x if x is not None else "")):
        valores = grupos[k]
        nao_nulos = [v for v in valores if v is not None]
        saida.append({
            chave: k, "linhas": len(valores), "n": len(nao_nulos),
            "soma": sum(nao_nulos) if nao_nulos else None,
            "media": round(sum(nao_nulos) / len(nao_nulos), 2) if nao_nulos else None,
            "maximo": max(nao_nulos) if nao_nulos else None,
        })
    return saida
```
O grupo `casa` é a armadilha principal: duas linhas, nenhum valor — a soma é `null`, e não 0. Um
relatório que faz `coalesce(sum(valor), 0)` sem pensar esconde a diferença entre "vendemos zero" e "não
sabemos quanto vendemos". Já `brinquedos` mostra o contrário: 0 é um valor, e entra na conta.

A média de `livros` é 40 (80 / 2 valores), não 26,67 (80 / 3 linhas). Se o negócio quer a média por
linha, é preciso ser explícito: `sum(valor) / count(*)`. Essas regras são idênticas no Spark, no
BigQuery e no Postgres — vale decorá-las uma vez.
:::

---
**Revisado em:** 2026-09-30
