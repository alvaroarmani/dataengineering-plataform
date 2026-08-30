# Exercício 05 — Carga idempotente de um dia (TRACK REAL · Postgres)

**Onde roda:** 🐳 Bancada Docker (Postgres real). Sem bancada? Faça o [Exercício 06](exercicio-06.md)
(mesma lógica, no navegador).

A task de uma DAG `@daily` é **dona de um dia**. Reprocessá-la (retry/backfill) deve
**substituir**, não duplicar. Implemente essa carga idempotente (overwrite da partição).

## Tabelas (o teste cria)
- `fato(data, id, valor)` — já tem `(2026-08-09, 1, 10)` de **outro dia** (deve permanecer).
- `batch(id, valor)` — os dados do dia `2026-08-10`: `(2,20),(3,30)`.

## Tarefa
Em [`exercicio-05/solucao.sql`](exercicio-05/solucao.sql), escreva **duas instruções**: apague
as linhas de `2026-08-10` e insira as do `batch` com essa data.

```bash
cd ambiente && docker compose up -d
pip install psycopg2-binary pytest
pytest -q modulos/09-orquestracao-airflow/exercicio-05
```
✅ O grader roda sua solução **duas vezes** e confere que o dia fica correto **sem duplicar** e
que `2026-08-09` permanece intacto.

## Dicas progressivas
:::{dropdown} Dica 1 — apague o dia
`DELETE FROM fato WHERE data = DATE '2026-08-10';`
:::
:::{dropdown} Dica 2 — insira o dia
`INSERT INTO fato (data, id, valor) SELECT DATE '2026-08-10', id, valor FROM batch;`
:::

## Solução comentada (abra só DEPOIS de passar)
:::{dropdown} Ver solução comentada
```sql
DELETE FROM fato WHERE data = DATE '2026-08-10';
INSERT INTO fato (data, id, valor)
SELECT DATE '2026-08-10', id, valor FROM batch;
```
Como a execução é dona do dia, reprocessá-la apaga só aquele dia e reinsere — **overwrite da
partição**. Rodar de novo converge para o mesmo estado (idempotente), e outros dias não são
tocados. É o que torna **backfill e retry** seguros no Airflow.
:::

---
**Revisado em:** 2026-08-29
