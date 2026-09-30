# Exercício 10 — Dimensionar partições e evitar arquivos pequenos

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
"Nem grandes demais, nem pequenas demais" (teoria 05): o alvo típico é ~128 MB por partição, com um
número de partições que seja múltiplo do número de cores (para as ondas de tarefas saírem cheias).
O outro lado do problema aparece na **escrita**: `df.write.partitionBy("data")` sem reorganizar os dados
faz **cada tarefa** escrever um arquivo **para cada data que ela contém** — 200 tarefas × 30 datas = 6.000
arquivinhos, que depois deixam toda leitura lenta. `repartition("data")` antes de gravar agrupa cada
data numa tarefa só.

## Tarefa
Em [`exercicio-10/solucao.py`](exercicio-10/solucao.py), implemente `planejar_particoes(tamanho_mb, cores, alvo_mb)` e `arquivos_gravados(datas_por_tarefa, repartition_por_data)`.

```bash
cd modulos/11-spark-lakehouse/exercicio-10
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — quantas partições
`ceil(tamanho / alvo)`, depois `max(..., cores)` e arredonde para o múltiplo de `cores` de cima: `ceil(n / cores) * cores`.
:::
:::{dropdown} Dica 2 — ondas
Com `n` múltiplo de `cores`, o número de ondas é `n // cores` — todas cheias.
:::
:::{dropdown} Dica 3 — arquivos
Sem repartition: soma, por tarefa, do número de datas distintas. Com repartition: só o número de datas distintas no total (`set().union(*...)`).
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
import math


def planejar_particoes(tamanho_mb: float, cores: int, alvo_mb: float = 128) -> dict:
    if cores < 1 or alvo_mb <= 0:
        raise ValueError("parâmetros inválidos")
    n = max(cores, math.ceil(tamanho_mb / alvo_mb))
    n = math.ceil(n / cores) * cores
    return {"particoes": n, "mb_por_particao": round(tamanho_mb / n, 1), "ondas": n // cores}


def arquivos_gravados(datas_por_tarefa: list, repartition_por_data: bool) -> int:
    if repartition_por_data:
        return len(set().union(*datas_por_tarefa)) if datas_por_tarefa else 0
    return sum(len(set(d)) for d in datas_por_tarefa)
```
50 GB com alvo de 128 MB dariam 391 partições; arredondando para o múltiplo de 32 cores, 416 — 13 ondas
cheias, em vez de 12 ondas cheias e uma com 7 tarefas (25 cores ociosos no fim do stage).

O teste dos arquivos pequenos é o problema mais comum de lakes: 6.000 arquivos de poucos KB por mês.
Cada leitura futura paga a abertura de todos eles (e, no S3, o custo por requisição, M21). A correção é
`df.repartition("data").write.partitionBy("data")` — 30 arquivos — ou, em tabelas Delta, um `OPTIMIZE`
periódico que compacta o que já foi escrito (exercício 07).
:::

---
**Revisado em:** 2026-09-30
