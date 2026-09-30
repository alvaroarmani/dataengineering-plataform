# Exercício 01 — Lazy evaluation: quantas vezes a fonte é lida (e o cache)

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
No Spark, transformações são **preguiçosas** (teoria 01): `filter`, `select`, `withColumn` só montam o
plano. Quem executa é a **ação** — `count`, `show`, `write`, `collect`. A consequência que surpreende:
**cada ação reexecuta o plano desde a fonte**. Um notebook com `df.count()`, depois `df.show()`, depois
`df.write...` lê o arquivo de origem três vezes.

`cache()` muda isso (teoria 05): ele também é preguiçoso — marca o DataFrame, e o resultado é
materializado na **primeira ação** depois dele; as ações seguintes reaproveitam.

## Tarefa
Em [`exercicio-01/solucao.py`](exercicio-01/solucao.py), implemente `simular(ops)`.

```bash
cd modulos/11-spark-lakehouse/exercicio-01
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — dois estados
Guarde `pendente` (cache marcado, ainda não materializado) e `materializado`. Transformações não mudam nada.
:::
:::{dropdown} Dica 2 — ação
Se já está materializado, a ação não lê a fonte. Senão, lê (+1) — e, se havia cache pendente, ele passa a materializado.
:::
:::{dropdown} Dica 3 — unpersist
Zera os dois estados: a próxima ação volta a ler a fonte.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
TRANSFORMACOES = {"filter", "select", "withColumn", "join", "groupBy", "orderBy", "distinct"}
ACOES = {"count", "show", "collect", "write", "first"}


def simular(ops: list) -> dict:
    acoes = leituras = 0
    pendente = materializado = False
    for op in ops:
        if op in TRANSFORMACOES:
            continue
        if op == "cache":
            pendente = not materializado
        elif op == "unpersist":
            pendente = materializado = False
        elif op in ACOES:
            acoes += 1
            if not materializado:
                leituras += 1
                if pendente:
                    materializado, pendente = True, False
        else:
            raise ValueError(f"operação desconhecida: {op}")
    return {"acoes": acoes, "leituras_da_fonte": leituras}
```
O segundo teste é o notebook típico: três ações, três leituras completas da fonte. Com um terabyte no
S3, são três terabytes lidos — e três vezes o custo. O `cache()` antes da primeira ação reduz a uma
leitura; colocado depois, só ajuda as ações seguintes.

Duas ressalvas de produção: cachear custa **memória** (se não couber, o Spark despeja partições e volta
a recomputar), e cache só compensa quando o intermediário é **reusado** e **caro de recomputar**. Um
pipeline linear com uma única ação (`write`) não ganha nada com `cache()`.
:::

---
**Revisado em:** 2026-09-30
