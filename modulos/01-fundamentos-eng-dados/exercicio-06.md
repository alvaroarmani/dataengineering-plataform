# Exercício 06 — Compressão por run-length: por que ordenar comprime

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
A teoria 02 diz que colunas comprimem bem porque os valores se repetem. Um dos truques mais simples
e usados (no Parquet, no BigQuery, em qualquer banco colunar) é o **run-length encoding (RLE)**: em
vez de guardar `SP, SP, SP, SP, RJ, RJ`, guarda-se `(SP, 4), (RJ, 2)`. Ele só funciona bem quando
valores iguais estão **juntos** — por isso a **ordenação** dos dados na escrita muda o tamanho do
arquivo. É a razão prática por trás de "clusterizar por estado" (M06).

## Tarefa
Em [`exercicio-06/solucao.py`](exercicio-06/solucao.py), implemente `rle(coluna)`, `desfazer_rle(pares)` e `taxa_compressao(coluna)`.

```bash
cd modulos/01-fundamentos-eng-dados/exercicio-06
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — um passe só
Percorra a coluna; se o valor é igual ao do último par, aumente a contagem; senão, abra um par novo.
:::
:::{dropdown} Dica 2 — desfazer
`[v] * n` repete o valor; `extend` junta tudo. Valide `n >= 1`.
:::
:::{dropdown} Dica 3 — a taxa
Valores originais divididos pelo número de pares. Cuidado com a coluna vazia.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def rle(coluna: list) -> list:
    pares = []
    for v in coluna:
        if pares and pares[-1][0] == v:
            pares[-1] = (v, pares[-1][1] + 1)
        else:
            pares.append((v, 1))
    return pares


def desfazer_rle(pares: list) -> list:
    out = []
    for v, n in pares:
        if n < 1:
            raise ValueError("repetição inválida")
        out.extend([v] * n)
    return out


def taxa_compressao(coluna: list) -> float:
    return round(len(coluna) / len(rle(coluna)), 2) if coluna else 1.0
```
Os mesmos 600 estados comprimem **1,09×** desordenados e **200×** ordenados. Nada mudou nos dados —
só a ordem. É por isso que warehouses **ordenam/clusterizam** as tabelas por colunas de baixa
cardinalidade (estado, data, categoria) na escrita: consultas que filtram por elas ficam mais
rápidas **e** o arquivo fica menor.

E o último teste mostra o limite: um id único por linha não se repete, e nenhuma ordenação ajuda.
Para esse tipo de coluna, os formatos usam outras técnicas (dicionário, *delta encoding*). Como
engenheiro, a lição é saber **quais** colunas comprimem — e escolher a ordenação pensando nelas.
:::

---
**Revisado em:** 2026-09-30
