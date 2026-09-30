# Exercício 08 — Ranqueamento por TF-IDF

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Ordenar resultados só pela frequência do termo (TF) premia documentos longos e palavras comuns: em
uma base de engenharia de dados, "dados" aparece em tudo e não diferencia nada. O **TF-IDF**
(teoria 04) pondera a frequência pela **raridade** do termo na coleção: um termo que aparece em
todos os documentos vale zero; um que aparece em poucos vale muito.

    tf(t, d)  = ocorrências de t em d / total de tokens de d
    idf(t)    = ln(N / df(t))      N = nº de documentos; df = nº de documentos com t
    score(d)  = soma de tf(t, d) * idf(t) para cada termo t da consulta

## Tarefa
Em [`exercicio-08/solucao.py`](exercicio-08/solucao.py), implemente `tf_idf(docs, consulta)`.

```bash
cd modulos/18-nosql-nao-relacional/exercicio-08
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — tokens e df
Tokenize cada documento uma vez. `df[t]` = em quantos documentos o termo aparece (use `set(tokens)` para não contar repetição dentro do mesmo doc).
:::
:::{dropdown} Dica 2 — o score
Para cada doc: soma de `ts.count(t) / len(ts) * math.log(n / df[t])`, só para termos com `df > 0` (um termo que não existe na coleção dividiria por zero).
:::
:::{dropdown} Dica 3 — filtrar e ordenar
Descarte scores 0 e ordene com `key=lambda x: (-x[1], x[0])`. Use `set` para os termos da consulta.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
import math
import re


def _tokens(texto: str) -> list:
    return [t for t in re.split(r"[^a-z0-9]+", texto.lower()) if t]


def tf_idf(docs: list, consulta: str) -> list:
    if not docs:
        return []
    toks = {d: _tokens(t) for d, t in docs}
    n = len(docs)
    termos = set(_tokens(consulta))
    df = {t: sum(t in set(ts) for ts in toks.values()) for t in termos}
    out = []
    for d, ts in toks.items():
        if not ts:
            continue
        score = sum(ts.count(t) / len(ts) * math.log(n / df[t]) for t in termos if df[t])
        if score > 0:
            out.append((d, round(score, 4)))
    return sorted(out, key=lambda x: (-x[1], x[0]))
```
O primeiro teste é o argumento do IDF: "dados" aparece nos 4 documentos, então `ln(4/4) = 0` — a
consulta não devolve nada, porque nada é **mais relevante** que o resto. Já "kafka" aparece em um
só documento e ganha peso máximo (`ln 4 ≈ 1,39`), e no doc `b` metade dos tokens é "kafka".

A normalização pelo tamanho (`tf` dividido pelo total de tokens) é o que faz o documento curto
vencer o longo no último teste. O **BM25**, padrão do Elasticsearch/OpenSearch, refina exatamente
esses dois pontos: satura o TF (a 10ª ocorrência vale menos que a 1ª) e controla o quanto o
tamanho do documento pesa.
:::

---
**Revisado em:** 2026-09-30
