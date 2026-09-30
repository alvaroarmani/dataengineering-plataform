# Exercício 06 — Backfill idempotente com overwrite por partição

**Onde roda:** 🟢 Browser ou 🐳 Bancada (Python puro).

## Contexto
O exercício 05 fez a carga idempotente de **um** dia no Postgres. Na operação, você raramente roda um
dia só: um bug descoberto hoje exige **reprocessar o último mês** (um *backfill*, teoria 03), e o
agendador pode reexecutar dias que já tinham rodado (*catchup*). A garantia que precisa valer: rodar
qualquer intervalo, quantas vezes for, produz o mesmo resultado — cada dia é **substituído**, nunca
acumulado. E um dia sem dados na fonte precisa **esvaziar** a partição (senão fica o dado velho).

## Tarefa
Em [`exercicio-06/solucao.py`](exercicio-06/solucao.py), implemente `carregar_dia(fato, dia, lote)` e `backfill(fato, fonte, inicio, fim)`.

```bash
cd modulos/09-orquestracao-airflow/exercicio-06
pytest -q
```

## Dicas progressivas
:::{dropdown} Dica 1 — overwrite
Remova tudo do `dia` (`[l for l in fato if l[0] != dia]`), adicione o lote marcado e ordene. Valide ids repetidos antes.
:::
:::{dropdown} Dica 2 — percorrer datas
`date.fromisoformat` e `timedelta(days=1)`; para cada dia, `fonte.get(dia, [])`.
:::
:::{dropdown} Dica 3 — dia sem dados
Com `[]`, `carregar_dia` apaga a partição e não adiciona nada — é exatamente o comportamento desejado: a fonte corrigida diz que aquele dia não teve vendas.
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```python
from datetime import date, timedelta


def carregar_dia(fato: list, dia: str, lote: list) -> list:
    ids = [i for i, _ in lote]
    if len(ids) != len(set(ids)):
        raise ValueError(f"lote de {dia} com id repetido")
    outros = [l for l in fato if l[0] != dia]
    return sorted(outros + [(dia, i, v) for i, v in lote])


def backfill(fato: list, fonte: dict, inicio: str, fim: str) -> list:
    d, f = date.fromisoformat(inicio), date.fromisoformat(fim)
    if d > f:
        raise ValueError("início depois do fim")
    while d <= f:
        dia = d.isoformat()
        fato = carregar_dia(fato, dia, fonte.get(dia, []))
        d += timedelta(days=1)
    return fato
```
O dia 12 é o caso que pega times desprevenidos: a fonte corrigida não tem vendas nesse dia (eram
testes de homologação que vazaram para produção). Um backfill que só **insere** o que vem da fonte
deixaria a venda fantasma lá para sempre; o overwrite por partição a remove.

O último teste é a propriedade que permite dormir tranquilo: rodar 10–11 e depois 11–12 (com o dia 11
reprocessado duas vezes) dá **exatamente** o mesmo resultado que rodar 10–12 uma vez. Com essa
garantia, `airflow dags backfill` e reexecuções manuais deixam de ser operações de risco.
:::

---
**Revisado em:** 2026-09-30
