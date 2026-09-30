# Exercício 06 — Stages e shuffles de um plano

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Cada transformação **wide** (teoria 03) — `groupBy`, `distinct`, `orderBy`, `repartition` e joins que
não são broadcast — exige um **shuffle**, e cada shuffle fecha um **stage**. Transformações narrow
(`filter`, `select`, `withColumn`) rodam encadeadas dentro do mesmo stage. Contar stages e shuffles de
cabeça, antes de rodar, é como você prevê o custo de um job — e percebe um shuffle desnecessário.

## Tarefa
Em [`exercicio-06/solucao.py`](exercicio-06/solucao.py), implemente `analisar_plano(plano, limite_broadcast_mb)`.

```bash
cd modulos/11-spark-lakehouse/exercicio-06
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — três categorias
Narrow (inclui `coalesce`) não conta; wide conta um shuffle; `join` depende do tamanho do outro lado.
:::
:::{dropdown} Dica 2 — stages
Cada shuffle é uma fronteira de stage: stages = shuffles + 1.
:::
:::{dropdown} Dica 3 — valide
Qualquer operação fora das listas é erro — um analisador que ignora o desconhecido dá números errados em silêncio.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
NARROW = {"filter", "select", "withColumn", "map", "union"}
WIDE = {"groupBy", "distinct", "orderBy", "repartition"}


def analisar_plano(plano: list, limite_broadcast_mb: float = 10) -> dict:
    shuffles = broadcasts = 0
    for passo in plano:
        op = passo[0]
        if op in NARROW or op == "coalesce":
            continue
        if op in WIDE:
            shuffles += 1
        elif op == "join":
            if passo[1] <= limite_broadcast_mb:
                broadcasts += 1
            else:
                shuffles += 1
        else:
            raise ValueError(f"passo desconhecido: {op}")
    return {"stages": shuffles + 1, "shuffles": shuffles, "broadcasts": broadcasts}
```
O plano do teste tem 3 shuffles: o join com a tabela de 50 MB, o `groupBy` e o `orderBy`. Subir o limite
de broadcast para 64 MB transforma o primeiro join em broadcast e elimina um stage inteiro — com 1 TB do
lado grande, é 1 TB a menos atravessando a rede.

Repare no `coalesce` no fim: ele reduz o número de partições (e de arquivos gravados) **sem** shuffle,
ao contrário do `repartition`. É a escolha certa para "gravar menos arquivos" quando o desbalanceamento
não é problema — o assunto do exercício 10.
:::

---
**Revisado em:** 2026-09-30
