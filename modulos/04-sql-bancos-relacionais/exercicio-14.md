# Exercício 14 — Poda por estatísticas (zone maps) com vários filtros

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
Particionar por data (teoria 07) poda partições inteiras. Mas bancos colunares vão além: cada bloco de
dados (uma partição, um *row group* do Parquet, um *micro-partition* do Snowflake) guarda o **mínimo e o
máximo** de cada coluna — um *zone map*. Uma consulta com `WHERE data BETWEEN ... AND valor > 1000` só
lê os blocos cujos intervalos **podem** conter linhas que passam em **todos** os filtros.

Dois detalhes decidem se a poda funciona: bloco **sem estatística** de uma coluna filtrada não pode ser
podado (o banco não sabe o que tem lá dentro), e os dados precisam estar **ordenados** pela coluna
filtrada — senão, todo bloco tem min e max espalhados e nada é podado.

## Tarefa
Em [`exercicio-14/solucao.py`](exercicio-14/solucao.py), implemente `blocos_lidos(blocos, filtros)` e `fracao_podada(blocos, filtros)`.

```bash
cd modulos/04-sql-bancos-relacionais/exercicio-14
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — sobreposição de intervalos
Um bloco `[mn, mx]` pode ter linhas na faixa `[lo, hi]` se `mn <= hi` **e** `mx >= lo` (limite `None` = sempre verdadeiro).
:::
:::{dropdown} Dica 2 — sem estatística
Se o bloco não tem `(min, max)` da coluna, trate como "pode ter": o bloco é lido.
:::
:::{dropdown} Dica 3 — todos os filtros
`all(...)` sobre os filtros: basta um filtro descartar o bloco para ele ser podado.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
def _sobrepoe(stats, faixa) -> bool:
    if stats is None:
        return True
    mn, mx = stats
    lo, hi = faixa
    return (hi is None or mn <= hi) and (lo is None or mx >= lo)


def blocos_lidos(blocos: list, filtros: dict) -> list:
    for col, (lo, hi) in filtros.items():
        if lo is not None and hi is not None and lo > hi:
            raise ValueError(f"faixa vazia em {col}")
    return [i for i, b in enumerate(blocos) if all(_sobrepoe(b.get(c), f) for c, f in filtros.items())]


def fracao_podada(blocos: list, filtros: dict) -> float:
    if not blocos:
        return 0.0
    return round(1 - len(blocos_lidos(blocos, filtros)) / len(blocos), 2)
```
O bloco 4 (maio) é lido na consulta por `valor >= 1000` só porque não tem estatística de valor — o banco
não pode provar que ele não tem vendas grandes. Estatísticas ausentes (arquivos gravados por ferramentas
que não as calculam, colunas de texto longo) desligam a poda silenciosamente.

O teste dos dados desordenados é a lição principal: com os mesmos 6 blocos, mas cada um contendo datas
do semestre inteiro, nenhum filtro de data poda nada. É por isso que se **ordena** (ou *clusteriza*, M06)
pela coluna mais filtrada na escrita — o mesmo motivo pelo qual ordenar melhora a compressão (M01).
:::

---
**Revisado em:** 2026-09-30
