# Exercício 01 — Custo pay-per-scan com mínimo por tabela

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
No modelo **pay-per-scan** (teoria 02), a consulta paga pelos bytes que lê. Parece simples — até
aparecerem as regras miúdas da fatura: arredondamento para cima e um **mínimo cobrado por tabela
referenciada**. Com elas, um dashboard que dispara milhares de consultas minúsculas por dia pode
custar mais do que uma única consulta grande.

O modelo deste exercício é **inspirado** no on-demand do BigQuery (arredonda cada tabela para o
MiB de cima, com mínimo de 10 MiB por tabela, e uma cota gratuita mensal em TiB). Os números exatos
mudam — confira sempre a página de preços atual; o método é o que importa.

## Tarefa
Em [`exercicio-01/solucao.py`](exercicio-01/solucao.py), implemente `bytes_cobrados(bytes_por_tabela)` e `custo_mensal(consultas, preco_por_tib, gratis_tib)`.

```bash
cd modulos/21-data-produto-finops/exercicio-01
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — uma tabela por vez
Para cada tabela: `math.ceil(b / MIB) * MIB` arredonda para cima; `max(..., MINIMO_POR_TABELA)` aplica o mínimo. Some tudo.
:::
:::{dropdown} Dica 2 — unidades binárias
1 MiB = 2**20 bytes e 1 TiB = 2**40 bytes. Converta o total do mês para TiB dividindo por `TIB`.
:::
:::{dropdown} Dica 3 — a cota
Desconte a cota e nunca deixe negativo: `max(0.0, tib - gratis_tib)`. Só então multiplique pelo preço e arredonde.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
import math

MIB = 2 ** 20
TIB = 2 ** 40
MINIMO_POR_TABELA = 10 * MIB


def bytes_cobrados(bytes_por_tabela: list) -> int:
    total = 0
    for b in bytes_por_tabela:
        if b < 0:
            raise ValueError("bytes negativos")
        total += max(math.ceil(b / MIB) * MIB, MINIMO_POR_TABELA)
    return total


def custo_mensal(consultas: list, preco_por_tib: float, gratis_tib: float = 1.0) -> float:
    tib = sum(bytes_cobrados(c) for c in consultas) / TIB
    return round(max(0.0, tib - gratis_tib) * preco_por_tib, 2)
```
O último teste é o achado típico de uma revisão FinOps: o painel lê de verdade uns 150 MB no mês
inteiro, mas **paga por 1,24 TiB** — porque cada uma das 43.200 execuções paga o mínimo em cada uma
das três tabelas. As correções clássicas: materializar o resultado numa tabela pequena (1 leitura
em vez de 3), usar cache de resultados, e reduzir a frequência de atualização ao que o negócio
realmente precisa.

Repare que a otimização de **performance** (a consulta já era rápida) e a de **custo** apontam
para lugares diferentes aqui. Custo é uma métrica própria — por isso precisa ser medida.
:::

---
**Revisado em:** 2026-09-30
