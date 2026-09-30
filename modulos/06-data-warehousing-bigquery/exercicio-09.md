# Exercício 09 — Bytes varridos: poda de coluna x poda de partição

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Num warehouse colunar e particionado (teoria 02), o custo de uma consulta depende de **duas podas
independentes**: a de **coluna** (ler só as colunas usadas) e a de **partição** (ler só as partições
que o filtro permite). Estimar os bytes antes de rodar é o que o *dry run* do BigQuery faz — e o que
você deveria fazer de cabeça antes de agendar uma consulta diária sobre uma tabela de terabytes.

Cuidado com o detalhe que derruba a poda de partição na prática: o filtro precisa ser **na própria
coluna de partição**. Filtrar por uma coluna derivada (ou por outra coluna de data) faz o warehouse
ler **todas** as partições.

## Tarefa
Em [`exercicio-09/solucao.py`](exercicio-09/solucao.py), implemente `bytes_varridos(tabela, consulta)` e `economia_pct(tabela, consulta)`.

```bash
cd modulos/06-data-warehousing-bigquery/exercicio-09
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — as colunas
`["*"]` vira a lista de todas as colunas; senão, valide que cada coluna existe e some os bytes.
:::
:::{dropdown} Dica 2 — a fração
Comece com `fracao = 1.0`. Só troque para `k / particoes` se houver filtro **e** ele for na `coluna_particao`.
:::
:::{dropdown} Dica 3 — economia
Compare com o total da tabela (todas as colunas, todas as partições): `100 * (1 - bytes / total)`.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def bytes_varridos(tabela: dict, consulta: dict) -> int:
    cols = tabela["bytes_por_coluna"]
    lidas = list(cols) if consulta["colunas"] == ["*"] else consulta["colunas"]
    faltando = [c for c in lidas if c not in cols]
    if faltando:
        raise ValueError(f"colunas inexistentes: {faltando}")
    fracao = 1.0
    filtro = consulta.get("filtro_particao")
    if filtro:
        if not 1 <= filtro["particoes"] <= tabela["particoes"]:
            raise ValueError("número de partições inválido")
        if filtro["coluna"] == tabela["coluna_particao"]:
            fracao = filtro["particoes"] / tabela["particoes"]
    return int(sum(cols[c] for c in lidas) * fracao)


def economia_pct(tabela: dict, consulta: dict) -> float:
    total = sum(tabela["bytes_por_coluna"].values())
    return round(100 * (1 - bytes_varridos(tabela, consulta) / total), 1)
```
A tabela tem 2,77 TB, e quase tudo está na coluna `payload_json`. Tirar essa coluna da consulta
economiza 96%; filtrar pela partição de 7 dias leva a economia para ~100% (0,64 GB). Já o `SELECT *`
de um único dia ainda lê 2,5 GB — mais que a semana inteira de duas colunas: **a poda de coluna
costuma valer mais que a de partição** quando existe uma coluna "gorda".

O teste do `data_ingestao` é o bug real: a consulta tem um filtro de data, parece otimizada, mas a
tabela é particionada por `data_evento` — o BigQuery lê as 1.095 partições. Olhe sempre o "This query
will process X" do dry run antes de agendar.
:::

---
**Revisado em:** 2026-09-30
